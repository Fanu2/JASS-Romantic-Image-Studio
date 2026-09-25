import csv, json, re, time, random
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

OUT = Path(__file__).with_name("romantic_stanzas_500.csv")
SEPARATION_OUT = Path(__file__).with_name("love_separation_150.csv")
CACHE = Path(__file__).with_name("poetry_source_cache.jsonl")
API = "https://datasets-server.huggingface.co/rows"
DATASET = "yoonholee/poetry-greats-public-domain"
CONFIG = "default"
SPLIT = "train"
PAGE_SIZE = 50
MAX_RETRIES = 7

LOVE_TERMS = {"love","loved","beloved","heart","hearts","kiss","kisses","darling","dear","desire","passion","tender","embrace","beauty","beautiful","sweet","soul","devotion","affection","romance"}
SEPARATION_TERMS = {"parted","parting","absence","absent","farewell","farewells","leave","leaving","left","lost","loss","alone","lonely","separation","separate","distance","away","waiting","wait","longing","yearning","tears","sorrow","grief","missing","missed","return","returning","departure","departed"}
TERMS = {"love":3,"loved":3,"beloved":4,"heart":3,"hearts":3,"kiss":3,"kisses":3,"darling":4,"dear":2,"desire":3,"passion":3,"longing":3,"tender":2,"embrace":3,"beauty":2,"beautiful":2,"sweet":2,"soul":3,"forever":3,"dream":2,"dreams":2,"moon":2,"stars":2,"night":2,"rose":2,"roses":2,"memory":2,"memories":2,"tears":2,"sorrow":2,"parted":3,"absence":3,"devotion":3,"affection":3,"romance":3}

def words(text):
    return re.findall(r"[A-Za-z']+", text.lower())

def score(text):
    return sum(TERMS.get(w, 0) for w in words(text or ""))

def love_separation_score(text):
    ws = set(words(text or ""))
    love = len(ws & LOVE_TERMS)
    sep = len(ws & SEPARATION_TERMS)
    return love * 3 + sep * 3 if love and sep else 0

def category(text):
    t = (text or "").lower()
    if love_separation_score(text) >= 6:
        return "Love & Separation"
    if any(w in t for w in ["parted","absence","farewell","tears","sorrow","longing"]):
        return "Longing & Separation"
    if any(w in t for w in ["moon","night","stars","dream"]):
        return "Dream & Night"
    if any(w in t for w in ["rose","roses","flower","flowers","beauty","sky","sea"]):
        return "Beauty & Nature"
    if any(w in t for w in ["love","beloved","heart","kiss","embrace","darling"]):
        return "Love & Devotion"
    return "Tender Reflection"

def split_stanzas(text):
    blocks = re.split(r"\n\s*\n+", (text or "").replace("\r", ""))
    out = []
    for b in blocks:
        lines = [x.strip() for x in b.splitlines() if x.strip()]
        wc = " ".join(lines).split()
        if 2 <= len(lines) <= 12 and 8 <= len(wc) <= 110:
            out.append("\n".join(lines))
    return out

def fetch_page(offset):
    params = urlencode({"dataset": DATASET, "config": CONFIG, "split": SPLIT, "offset": offset, "length": PAGE_SIZE})
    req = Request(API + "?" + params, headers={
        "User-Agent": "JASS-Romantic-Image-Studio/5.5",
        "Accept": "application/json",
    })
    with urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))

def load_cache():
    rows = []
    if CACHE.exists():
        with CACHE.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows

def append_cache(rows):
    if not rows:
        return
    with CACHE.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def fetch_all_source_rows():
    cached = load_cache()
    offset = len(cached)
    if cached:
        print(f"Resuming from local cache: {offset} source records already saved.")
    else:
        print("No local cache found; starting download from source.")

    total = None
    while True:
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                payload = fetch_page(offset)
                last_error = None
                break
            except HTTPError as e:
                last_error = e
                if e.code == 429:
                    wait = min(120, 10 * (2 ** attempt)) + random.uniform(0, 3)
                    print(f"HTTP 429 rate limit at offset {offset}. Waiting {wait:.0f}s before retry {attempt+1}/{MAX_RETRIES}...")
                    time.sleep(wait)
                elif e.code in (500, 502, 503, 504):
                    wait = min(60, 5 * (2 ** attempt)) + random.uniform(0, 2)
                    print(f"HTTP {e.code} at offset {offset}. Waiting {wait:.0f}s before retry {attempt+1}/{MAX_RETRIES}...")
                    time.sleep(wait)
                else:
                    print(f"HTTP {e.code} at offset {offset}: {e}")
                    break
            except (URLError, TimeoutError) as e:
                last_error = e
                wait = min(60, 5 * (2 ** attempt)) + random.uniform(0, 2)
                print(f"Network error at offset {offset}. Waiting {wait:.0f}s before retry {attempt+1}/{MAX_RETRIES}...")
                time.sleep(wait)
        if last_error is not None:
            print("Download paused safely. Your downloaded pages are saved in:")
            print(CACHE)
            print("Run this builder again later; it will resume from the cache instead of starting over.")
            return cached

        if total is None:
            total = payload.get("num_rows_total")
            print("Source rows:", total)

        rows = payload.get("rows", [])
        if not rows:
            break
        page_rows = [wrapper.get("row", {}) for wrapper in rows]
        append_cache(page_rows)
        cached.extend(page_rows)
        offset += len(page_rows)
        print(f"Downloaded and cached {offset} source records.")
        if total is not None and offset >= total:
            break
        if len(page_rows) < PAGE_SIZE:
            break
        time.sleep(1.0)
    return cached

def build_candidates(source_rows):
    candidates = []
    for n, row in enumerate(source_rows, 1):
        text = row.get("poem_text", "") or ""
        author = str(row.get("author", "") or "")
        poem = str(row.get("poem_title", "") or "")
        gid = row.get("gutenberg_id", "") or ""
        for stanza in split_stanzas(text):
            if score(stanza) < 2:
                continue
            candidates.append({
                "author": author,
                "poem_title": poem,
                "category": category(stanza),
                "mood": "Romantic",
                "stanza": stanza,
                "source": f"https://www.gutenberg.org/ebooks/{gid}" if gid else "",
                "license": "Public domain / CC0 dataset"
            })
        if n % 500 == 0:
            print(f"Processed {n} cached source records; found {len(candidates)} candidates.")
    return candidates

def main():
    print("JASS Romantic Image Studio — Literary Dataset Builder V5.5")
    print("Source:", DATASET)
    source_rows = fetch_all_source_rows()
    if not source_rows:
        print("No source records were downloaded.")
        return

    candidates = build_candidates(source_rows)
    print(f"Total source records available: {len(source_rows)}")
    print(f"Total candidates: {len(candidates)}")

    def sort_text(value):
        return str(value or "").strip()

    def select(pool, limit, author_cap, poem_cap, rank_key):
        chosen, author_count, poem_count, seen = [], {}, {}, set()
        for r in sorted(pool, key=rank_key):
            key = (sort_text(r.get("author")), sort_text(r.get("poem_title")), sort_text(r.get("stanza")))
            if key in seen:
                continue
            author = sort_text(r.get("author")); poem = sort_text(r.get("poem_title")); stanza = sort_text(r.get("stanza"))
            if author_count.get(author, 0) >= author_cap:
                continue
            pkey = (author, poem)
            if poem_count.get(pkey, 0) >= poem_cap:
                continue
            chosen.append(r); seen.add(key)
            author_count[author] = author_count.get(author, 0) + 1
            poem_count[pkey] = poem_count.get(pkey, 0) + 1
            if len(chosen) >= limit:
                break
        return chosen

    selected = select(candidates, 500, 35, 5,
                      lambda x: (-score(x.get("stanza") or ""), sort_text(x.get("author")), sort_text(x.get("poem_title"))))
    separation_candidates = [r for r in candidates if love_separation_score(r.get("stanza") or "") >= 6]
    love_separation = select(separation_candidates, 150, 20, 4,
                             lambda x: (-love_separation_score(x.get("stanza") or ""), -score(x.get("stanza") or ""), sort_text(x.get("author")), sort_text(x.get("poem_title"))))

    print("Love & Separation candidates:", len(separation_candidates))
    if len(selected) < 500:
        print(f"Only {len(selected)} suitable stanzas were found; authentic available records will be written.")
    if len(love_separation) < 150:
        print(f"Only {len(love_separation)} Love & Separation stanzas were found; authentic available records will be written.")

    fields = ["id","image_slot","author","poem_title","category","mood","stanza","source","license"]
    def write_csv(path, rows, prefix):
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
            for i, r in enumerate(rows, 1):
                w.writerow({"id": f"{prefix}{i:03d}", "image_slot": f"image_{i:03d}", **r})

    write_csv(OUT, selected, "S")
    write_csv(SEPARATION_OUT, love_separation, "LS")
    print("Created:", OUT)
    print("Records:", len(selected))
    print("Created:", SEPARATION_OUT)
    print("Love & Separation records:", len(love_separation))
    print("The source cache is retained so future rebuilds do not redownload the dataset.")
    print("Now restart the app or click ↻ Reload.")

if __name__ == "__main__":
    main()
