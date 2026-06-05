"""
Wikidata SPARQL Client for Technology Mapping

Queries Wikidata's doctoral advisor (P184) property and related academic
genealogy data. Used by the technology-mapping skill to establish
mentor-student relationships.

API: https://query.wikidata.org/sparql (free, no auth required)
Coverage: ~380,000 doctoral advisor entries (as of 2026-03)
"""

import requests
import hashlib
import json
import logging
import time
from collections import OrderedDict
from typing import Optional

logger = logging.getLogger(__name__)

WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "TechMapping-Skill/2.1.0 (technology-mapping; research)"
REQUEST_DELAY = 1.0  # seconds between requests (polite rate limiting)
MAX_RETRIES = 3      # exponential backoff retries for transient failures
CACHE_MAX_SIZE = 200 # max cached queries

_last_request_time = 0.0
_cache: OrderedDict[str, list[dict]] = OrderedDict()


def _escape_sparql(s: str) -> str:
    """Escape special chars for SPARQL string literals.
    
    Prevents injection and handles names like O'Brien, "quoted" names, etc.
    """
    return (s.replace('\\', '\\\\')
             .replace('"', '\\"')
             .replace("'", "\\\'")
             .replace('\n', '\\n')
             .replace('\r', '\\r')
             .replace('\t', '\\t'))


def _cache_key(query: str) -> str:
    """Generate a compact hash key for a SPARQL query string."""
    return hashlib.sha256(query.strip().encode()).hexdigest()


def _cache_put(key: str, value: list[dict]) -> None:
    """Insert into LRU-style cache with size limit."""
    global _cache
    _cache[key] = value
    while len(_cache) > CACHE_MAX_SIZE:
        _cache.popitem(last=False)  # evict oldest


def _sparql_query(query: str, use_cache: bool = True) -> list[dict]:
    """Execute a SPARQL query against Wikidata and return bindings.
    
    Features:
    - Rate limiting (1 req/s)
    - Exponential backoff retry (3 attempts) for 429/503/timeout
    - In-memory LRU cache (max 200 entries)
    """
    global _last_request_time

    # Cache check
    key = _cache_key(query)
    if use_cache and key in _cache:
        return _cache[key]

    for attempt in range(MAX_RETRIES):
        # Rate limiting
        elapsed = time.time() - _last_request_time
        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)

        try:
            r = requests.get(
                WIKIDATA_SPARQL_ENDPOINT,
                params={"query": query, "format": "json"},
                headers={"User-Agent": USER_AGENT},
                timeout=30,
            )
            _last_request_time = time.time()

            if r.status_code == 200:
                data = r.json()
                results = data.get("results", {}).get("bindings", [])
                if use_cache:
                    _cache_put(key, results)
                return results

            if r.status_code in (429, 503) and attempt < MAX_RETRIES - 1:
                wait = 2 ** (attempt + 1)  # 2s, 4s
                logger.warning(
                    "HTTP %d, retrying in %ds (attempt %d/%d)",
                    r.status_code, wait, attempt + 1, MAX_RETRIES,
                )
                time.sleep(wait)
                continue

            logger.error("SPARQL query failed: HTTP %d", r.status_code)
            return []

        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** (attempt + 1)
                logger.warning(
                    "Timeout, retrying in %ds (attempt %d/%d)",
                    wait, attempt + 1, MAX_RETRIES,
                )
                time.sleep(wait)
                continue
            logger.error("SPARQL query timeout after all retries")
            return []

        except Exception as e:
            logger.error("SPARQL query error: %s", e)
            return []

    return []


def _extract_label(binding: dict, key: str) -> str:
    """Extract a label value from a SPARQL binding."""
    return binding.get(key, {}).get("value", "")


def _extract_id(binding: dict, key: str) -> str:
    """Extract a Wikidata QID from a SPARQL binding URI."""
    uri = binding.get(key, {}).get("value", "")
    if "/entity/" in uri:
        return uri.split("/entity/")[-1]
    return uri


def query_doctoral_advisor(person_name: str, try_chinese: bool = True) -> list[dict]:
    """
    Query Wikidata for a person's doctoral advisor(s).
    Searches both English and Chinese labels for better coverage of Chinese scholars.

    Args:
        person_name: Full name of the person (e.g., "Geoffrey Hinton" or "施路平")
        try_chinese: If True and English search fails, also try Chinese label search

    Returns:
        List of dicts with keys: advisor_name, advisor_qid, person_qid
        Empty list if not found.
    """
    safe_name = _escape_sparql(person_name)

    # Try English label first
    query_en = f'''
    SELECT ?person ?personLabel ?advisor ?advisorLabel WHERE {{
      ?person rdfs:label "{safe_name}"@en .
      ?person wdt:P184 ?advisor .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,zh" }}
    }}
    LIMIT 10
    '''
    bindings = _sparql_query(query_en)

    # If no results and try_chinese is enabled, try Chinese label
    if not bindings and try_chinese:
        query_zh = f'''
        SELECT ?person ?personLabel ?advisor ?advisorLabel WHERE {{
          ?person rdfs:label "{safe_name}"@zh .
          ?person wdt:P184 ?advisor .
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "zh,en" }}
        }}
        LIMIT 10
        '''
        bindings = _sparql_query(query_zh)

    results = []
    for b in bindings:
        results.append({
            "advisor_name": _extract_label(b, "advisorLabel"),
            "advisor_qid": _extract_id(b, "advisor"),
            "person_name": _extract_label(b, "personLabel"),
            "person_qid": _extract_id(b, "person"),
        })
    return results


def query_students(advisor_name: str = None, advisor_qid: str = None) -> list[dict]:
    """
    Query Wikidata for all doctoral students of a given advisor.

    Args:
        advisor_name: Full name of the advisor (e.g., "Geoffrey Hinton")
        advisor_qid: Wikidata QID of the advisor (e.g., "Q192620")
                     If provided, takes priority over advisor_name.

    Returns:
        List of dicts with keys: student_name, student_qid
    """
    if advisor_qid:
        filter_clause = f"wd:{advisor_qid}"
    elif advisor_name:
        safe_name = _escape_sparql(advisor_name)
        # First find advisor's QID by name (try both en and zh)
        find_query = f'''
        SELECT ?advisor WHERE {{
          {{ ?advisor rdfs:label "{safe_name}"@en . }}
          UNION
          {{ ?advisor rdfs:label "{safe_name}"@zh . }}
          ?advisor wdt:P106 ?occupation .
          FILTER(?occupation IN (
            wd:Q1622272,   # university professor
            wd:Q901,       # scientist
            wd:Q1650915,   # researcher
            wd:Q593644     # professor (generic)
          ))
        }} LIMIT 1
        '''
        bindings = _sparql_query(find_query)
        if not bindings:
            return []
        filter_clause = f"wd:{_extract_id(bindings[0], 'advisor')}"
    else:
        return []

    query = f'''
    SELECT ?student ?studentLabel WHERE {{
      ?student wdt:P184 {filter_clause} .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,zh" }}
    }}
    LIMIT 50
    '''
    bindings = _sparql_query(query)

    return [
        {
            "student_name": _extract_label(b, "studentLabel"),
            "student_qid": _extract_id(b, "student"),
        }
        for b in bindings
    ]


def query_person_info(person_name: str, expected_field: str = None) -> Optional[dict]:
    """
    Query Wikidata for a person's basic academic info.
    Uses two lightweight queries instead of one complex one to avoid timeouts.
    Searches both English and Chinese labels.

    Args:
        person_name: Full name of the person
        expected_field: Optional field/domain keyword for disambiguation.
                        When multiple Q-entities match the name, prefer the one
                        whose wdt:P101 (field of work) contains this keyword.

    Returns dict with: qid, name, description, fields, institutions,
                       doctoral_advisors, doctoral_students_count
    """
    safe_name = _escape_sparql(person_name)

    # Step 1: Find person QID and basic info (try en then zh)
    query1 = f'''
    SELECT ?person ?personLabel ?personDescription WHERE {{
      {{ ?person rdfs:label "{safe_name}"@en . }}
      UNION
      {{ ?person rdfs:label "{safe_name}"@zh . }}
      ?person wdt:P31 wd:Q5 .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,zh" }}
    }} LIMIT 5
    '''
    bindings1 = _sparql_query(query1)
    if not bindings1:
        return None

    # Disambiguation: pick best match
    best = bindings1[0]
    if expected_field and len(bindings1) > 1:
        field_lower = expected_field.lower()
        for candidate in bindings1:
            desc = _extract_label(candidate, "personDescription").lower()
            if field_lower in desc:
                best = candidate
                logger.info(
                    "Disambiguated '%s' → matched description containing '%s'",
                    person_name, expected_field,
                )
                break

    b = best
    qid = _extract_id(b, "person")

    # Step 2: Get academic properties for this specific QID
    query2 = f'''
    SELECT
      ?fieldLabel ?instLabel ?advisorLabel
      (COUNT(DISTINCT ?student) AS ?studentCount)
    WHERE {{
      OPTIONAL {{ wd:{qid} wdt:P101 ?field . }}
      OPTIONAL {{ wd:{qid} wdt:P108 ?inst . }}
      OPTIONAL {{ wd:{qid} wdt:P184 ?advisor . }}
      OPTIONAL {{ ?student wdt:P184 wd:{qid} . }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,zh" }}
    }}
    GROUP BY ?fieldLabel ?instLabel ?advisorLabel
    LIMIT 20
    '''
    bindings2 = _sparql_query(query2)

    fields = set()
    institutions = set()
    advisors = set()
    student_count = 0

    for b2 in bindings2:
        f = _extract_label(b2, "fieldLabel")
        i = _extract_label(b2, "instLabel")
        a = _extract_label(b2, "advisorLabel")
        sc = _extract_label(b2, "studentCount")
        if f: fields.add(f)
        if i: institutions.add(i)
        if a: advisors.add(a)
        if sc: student_count = max(student_count, int(sc))

    # Post-hoc disambiguation: if expected_field given, verify match
    if expected_field and fields:
        field_lower = expected_field.lower()
        if not any(field_lower in fl.lower() for fl in fields):
            logger.warning(
                "Disambiguation warning: '%s' fields %s don't match expected '%s'",
                person_name, fields, expected_field,
            )

    return {
        "qid": qid,
        "name": _extract_label(b, "personLabel"),
        "description": _extract_label(b, "personDescription"),
        "fields": ", ".join(sorted(fields)),
        "institutions": ", ".join(sorted(institutions)),
        "doctoral_advisors": ", ".join(sorted(advisors)),
        "doctoral_students_count": student_count,
    }


def batch_query_advisors(names: list[str]) -> dict[str, list[dict]]:
    """
    Batch query doctoral advisors for multiple people.
    Uses SPARQL VALUES clause for efficient single-query batch lookup,
    then falls back to individual queries for names not found.

    Args:
        names: List of person names

    Returns:
        Dict mapping each name to its query_doctoral_advisor() result.
    """
    if not names:
        return {}

    # Phase 1: Batch query using VALUES (English labels)
    safe_names = [_escape_sparql(n) for n in names]
    values_str = " ".join(f'"{sn}"@en' for sn in safe_names)

    batch_query = f'''
    SELECT ?name ?person ?personLabel ?advisor ?advisorLabel WHERE {{
      VALUES ?name {{ {values_str} }}
      ?person rdfs:label ?name .
      ?person wdt:P184 ?advisor .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,zh" }}
    }}
    '''
    bindings = _sparql_query(batch_query)

    # Group results by matched name
    results: dict[str, list[dict]] = {name: [] for name in names}
    matched_names = set()

    for b in bindings:
        person_label = _extract_label(b, "personLabel")
        advisor_name = _extract_label(b, "advisorLabel")
        advisor_qid = _extract_id(b, "advisor")
        person_qid = _extract_id(b, "person")

        # Match back to original names (case-insensitive, exact match only)
        for name in names:
            if name.lower() == person_label.lower():
                matched_names.add(name)
                results[name].append({
                    "advisor_name": advisor_name,
                    "advisor_qid": advisor_qid,
                    "person_name": person_label,
                    "person_qid": person_qid,
                })
                break

    # Phase 2: Individual fallback for unmatched names (incl. Chinese labels)
    unmatched = [n for n in names if n not in matched_names]
    if unmatched:
        logger.info("Batch missed %d/%d names, falling back to individual queries", len(unmatched), len(names))
        for name in unmatched:
            results[name] = query_doctoral_advisor(name)

    return results


def clear_cache():
    """Clear the in-memory query cache."""
    global _cache
    _cache.clear()


# --- CLI usage ---
if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="[wikidata] %(levelname)s: %(message)s")

    if len(sys.argv) < 2:
        print("Usage: python wikidata_client.py <person_name>")
        print("       python wikidata_client.py --students <advisor_name>")
        print("       python wikidata_client.py --info <person_name>")
        sys.exit(1)

    if sys.argv[1] == "--students":
        name = " ".join(sys.argv[2:])
        print(f"Searching students of: {name}")
        students = query_students(advisor_name=name)
        if students:
            print(f"Found {len(students)} students:")
            for s in students:
                print(f"  {s['student_name']} ({s['student_qid']})")
        else:
            print("  No students found in Wikidata")

    elif sys.argv[1] == "--info":
        name = " ".join(sys.argv[2:])
        print(f"Querying info for: {name}")
        info = query_person_info(name)
        if info:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print("  Not found in Wikidata")

    else:
        name = " ".join(sys.argv[1:])
        print(f"Searching doctoral advisor(s) of: {name}")
        advisors = query_doctoral_advisor(name)
        if advisors:
            for a in advisors:
                print(f"  {a['person_name']} → advisor: {a['advisor_name']} ({a['advisor_qid']})")
        else:
            print("  No advisor found in Wikidata")
