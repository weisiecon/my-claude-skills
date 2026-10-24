#!/usr/bin/env python3
"""Fetch title, year, venue, and abstract for papers from free scholarly APIs.

Usage:
  python3 fetch_abstract.py --doi 10.1093/qje/qjt031
  python3 fetch_abstract.py --doi-file dois.txt          (one DOI per line)
  python3 fetch_abstract.py --query "Chodorow-Reich employment credit market disruptions 2014"
  python3 fetch_abstract.py --bib refs.bib [--keys key1,key2,...]
  python3 fetch_abstract.py --url https://www.iza.org/publications/dp/16000

DOI mode tries Crossref, then OpenAlex, then Semantic Scholar, then the
publisher's landing page (meta tags), and stops at the first source that
returns an abstract. Query mode returns up to three Crossref
candidates (DOI, title, year, venue) so that the caller can pick the right one.
Bib mode reads the .bib file; for entries without a DOI it searches Crossref by
authors, title, and year, accepts the best candidate only if its title is close
to the .bib title, and then fetches the abstract.
Output is one JSON object per line. Only the Python standard library is used.
"""
import argparse
import difflib
import html
import json
import re
import sys
import time
from html.parser import HTMLParser
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "lit-review-verify/1.0 (Claude Code skill)"
TIMEOUT_SECONDS = 20
PAUSE_SECONDS = 0.3  # polite delay between papers in batch mode


def get_json(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.load(response)


def clean_text(text):
    """Strip JATS/HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"^Abstract\s*[:.]?\s*", "", text, flags=re.IGNORECASE)


def first(values):
    return values[0] if values else ""


def from_crossref(doi):
    message = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    date_parts = (message.get("issued") or {}).get("date-parts") or [[None]]
    return {
        "title": clean_text(first(message.get("title"))),
        "year": date_parts[0][0] if date_parts[0] else None,
        "venue": first(message.get("container-title")),
        "abstract": clean_text(message.get("abstract", "")),
    }


def from_openalex(doi):
    work = get_json("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))
    positions = {}
    for word, indexes in (work.get("abstract_inverted_index") or {}).items():
        for index in indexes:
            positions[index] = word
    source = ((work.get("primary_location") or {}).get("source") or {})
    return {
        "title": work.get("title") or "",
        "year": work.get("publication_year"),
        "venue": source.get("display_name") or "",
        "abstract": clean_text(" ".join(positions[i] for i in sorted(positions))),
        "cited_by_count": work.get("cited_by_count"),
    }


def from_semantic_scholar(doi):
    fields = "title,year,venue,abstract,citationCount"
    paper = get_json(
        "https://api.semanticscholar.org/graph/v1/paper/DOI:"
        + urllib.parse.quote(doi)
        + "?fields="
        + fields
    )
    return {
        "title": paper.get("title") or "",
        "year": paper.get("year"),
        "venue": paper.get("venue") or "",
        "abstract": clean_text(paper.get("abstract") or ""),
        "cited_by_count": paper.get("citationCount"),
    }


SOURCES = [("crossref", from_crossref), ("openalex", from_openalex), ("semanticscholar", from_semantic_scholar)]


def lookup_doi(doi):
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi.strip(), flags=re.IGNORECASE)
    result = {"doi": doi, "source": None, "title": "", "year": None, "venue": "", "abstract": "", "tried": []}
    for name, fetch in SOURCES:
        try:
            record = fetch(doi)
        except urllib.error.HTTPError as error:
            result["tried"].append(f"{name}: HTTP {error.code}")
            continue
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as error:
            result["tried"].append(f"{name}: {type(error).__name__}")
            continue
        result["tried"].append(f"{name}: ok" + ("" if record["abstract"] else " (no abstract)"))
        for key in ("title", "year", "venue"):
            if not result[key] and record.get(key):
                result[key] = record[key]
        if record.get("cited_by_count") is not None:
            result["cited_by_count"] = record["cited_by_count"]
        if record["abstract"]:
            result["source"] = name
            result["abstract"] = record["abstract"]
            break
    if not result["abstract"]:
        # Fourth source: the publisher's landing page. Springer and others put the full
        # abstract in dc.description; the plain "description" tag is skipped because
        # sites such as NBER use it for a generic site blurb.
        page = from_url("https://doi.org/" + urllib.parse.quote(doi))
        for name in ("citation_abstract", "dc.description", "og:description"):
            text = page["candidates"].get(name, "")
            if len(text) >= 100:
                result["source"], result["abstract"] = f"landing page ({name})", text
                break
        result["tried"].append("landing page: " + (page.get("error") or ("ok" if result["abstract"] else "no abstract tag")))
    return result


def search_crossref(query, rows=3):
    params = urllib.parse.urlencode(
        {"query.bibliographic": query, "rows": rows, "select": "DOI,title,issued,container-title,score"}
    )
    try:
        items = get_json("https://api.crossref.org/works?" + params)["message"]["items"]
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as error:
        return {"query": query, "error": type(error).__name__, "candidates": []}
    candidates = []
    for item in items:
        date_parts = (item.get("issued") or {}).get("date-parts") or [[None]]
        candidates.append(
            {
                "doi": item.get("DOI"),
                "title": clean_text(first(item.get("title"))),
                "year": date_parts[0][0] if date_parts[0] else None,
                "venue": first(item.get("container-title")),
                "score": item.get("score"),
            }
        )
    return {"query": query, "candidates": candidates}


META_NAMES = ("citation_abstract", "dc.description", "og:description", "description")


class MetaCollector(HTMLParser):
    """Collect <meta name=... content=...> values that may hold an abstract."""

    def __init__(self):
        super().__init__()
        self.found = {}

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        attributes = {k.lower(): (v or "") for k, v in attrs}
        name = (attributes.get("name") or attributes.get("property") or "").lower()
        if name in META_NAMES and attributes.get("content") and name not in self.found:
            self.found[name] = clean_text(attributes["content"])


def from_url(url):
    """Read abstract candidates from a landing page's meta tags (works for IZA, Springer, and others)."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; " + USER_AGENT + ")"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            page = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        return {"url": url, "error": f"HTTP {error.code}", "candidates": {}}
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        return {"url": url, "error": type(error).__name__, "candidates": {}}
    collector = MetaCollector()
    collector.feed(page)
    # Some sites (for example NBER) put a generic site description here; the caller must check.
    return {"url": url, "candidates": {name: collector.found[name] for name in META_NAMES if name in collector.found}}


TITLE_MATCH_THRESHOLD = 0.85  # minimum similarity between .bib title and Crossref title


def parse_bib(path):
    """Minimal BibTeX reader: returns {key: {field: value}} with brace-aware values."""
    text = open(path, encoding="utf-8", errors="replace").read()
    entries = {}
    for match in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        if match.group(1).lower() in ("comment", "preamble", "string"):
            continue
        key, position, fields = match.group(2), match.end(), {}
        while True:
            field = re.compile(r"\s*(\w[\w-]*)\s*=\s*").match(text, position)
            if not field:
                break
            name, position = field.group(1).lower(), field.end()
            if position < len(text) and text[position] in "{\"":
                closer, depth, start = ("}" if text[position] == "{" else "\""), 0, position
                while position < len(text):
                    char = text[position]
                    if char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                    if (closer == "}" and depth == 0) or (closer == "\"" and char == "\"" and position > start and depth == 0):
                        break
                    position += 1
                value, position = text[start + 1:position], position + 1
            else:
                bare = re.compile(r"[^,}\s]+").match(text, position)
                value, position = (bare.group(0), bare.end()) if bare else ("", position)
            fields[name] = value
            separator = re.compile(r"\s*,").match(text, position)
            if not separator:
                break
            position = separator.end()
        entries[key] = fields
    return entries


def strip_latex(text):
    text = re.sub(r"\\[a-zA-Z]+\s*", " ", text or "")
    return re.sub(r"\s+", " ", text.replace("{", "").replace("}", "").replace("~", " ")).strip()


def normalized(title):
    return re.sub(r"[^a-z0-9 ]", "", strip_latex(title).lower()).strip()


def surnames(authors):
    names = []
    for person in re.split(r"\s+and\s+", strip_latex(authors)):
        person = person.strip()
        if person:
            names.append(person.split(",")[0].strip() if "," in person else person.split()[-1])
    return " ".join(names[:3])


def lookup_bib_entry(key, fields):
    title, year = strip_latex(fields.get("title", "")), re.sub(r"\D", "", fields.get("year", ""))[:4]
    base = {"key": key, "bib_title": title, "bib_year": year or None}
    if fields.get("doi"):
        return {**base, "match": "doi in .bib", **lookup_doi(strip_latex(fields["doi"]))}
    if not title:
        return {**base, "match": "unresolved (no title in .bib)", "abstract": ""}
    found = search_crossref(" ".join(filter(None, [surnames(fields.get("author", "")), title, year])), rows=5)
    scored = []
    for candidate in found.get("candidates", []):
        score = difflib.SequenceMatcher(None, normalized(title), normalized(candidate["title"])).ratio()
        scored.append((score, candidate))
    good = [(s, c) for s, c in scored if s >= TITLE_MATCH_THRESHOLD and c.get("doi")]
    if not good:
        best_score, best = max(scored, key=lambda pair: pair[0], default=(0.0, None))
        nearest = best["title"] if best else None
        return {**base, "match": f"unresolved (best title similarity {best_score:.2f})", "nearest_title": nearest, "abstract": ""}

    # The same title often exists as a working paper and as the published article.
    # Prefer the version whose year is closest to the .bib year, then the closest title.
    def rank(pair):
        score, candidate = pair
        gap = abs(int(year) - candidate["year"]) if year and candidate.get("year") else 99
        return (gap, -score)

    good.sort(key=rank)
    primary_score, primary = good[0]
    result = {**base, "match": f"crossref title match {primary_score:.2f}", **lookup_doi(primary["doi"])}
    others = [c for _, c in good[1:]]
    if others:
        result["other_versions"] = [{"doi": c["doi"], "year": c.get("year"), "venue": c.get("venue")} for c in others]
    if not result["abstract"]:
        for candidate in others:
            borrowed = lookup_doi(candidate["doi"])
            if borrowed["abstract"]:
                result["abstract"] = borrowed["abstract"]
                result["abstract_from"] = f"{candidate['doi']} ({candidate.get('venue') or 'other version'}, {candidate.get('year')})"
                result["source"] = borrowed["source"]
                break
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doi", help="a single DOI")
    group.add_argument("--doi-file", help="text file with one DOI per line")
    group.add_argument("--query", help="free-text bibliographic query (authors, title, year)")
    group.add_argument("--bib", help="a .bib file; resolves every entry, or only --keys")
    group.add_argument("--url", help="a paper's landing page; returns abstract candidates from its meta tags")
    parser.add_argument("--keys", help="comma-separated citation keys to resolve (bib mode only)")
    args = parser.parse_args()

    if args.url:
        print(json.dumps(from_url(args.url), ensure_ascii=False))
        return
    if args.query:
        print(json.dumps(search_crossref(args.query), ensure_ascii=False))
        return
    if args.bib:
        entries = parse_bib(args.bib)
        keys = [k.strip() for k in args.keys.split(",") if k.strip()] if args.keys else list(entries)
        for position, key in enumerate(keys):
            if position:
                time.sleep(PAUSE_SECONDS)
            if key not in entries:
                print(json.dumps({"key": key, "match": "key not found in .bib", "abstract": ""}), flush=True)
                continue
            print(json.dumps(lookup_bib_entry(key, entries[key]), ensure_ascii=False), flush=True)
        return
    if args.doi:
        dois = [args.doi]
    else:
        with open(args.doi_file, encoding="utf-8") as handle:
            dois = [line.strip() for line in handle if line.strip() and not line.startswith("#")]
    for position, doi in enumerate(dois):
        if position:
            time.sleep(PAUSE_SECONDS)
        print(json.dumps(lookup_doi(doi), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    sys.exit(main())
