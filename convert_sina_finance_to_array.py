import json
from pathlib import Path

src = Path("sina_finance_news.json")
dst = Path("sina_finance_array.json")

items = []
with src.open("r", encoding="utf-8") as f:
    for idx, line in enumerate(f, start=1):
        raw = line
        line = line.strip()
        if not line:
            # skip empty / whitespace-only lines
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            # Print debug info and skip this line
            print(f"Skipping line {idx} due to JSON error: {e}")
            print(f"  Line content (first 80 chars): {raw[:80]!r}")
            continue
        items.append(obj)

with dst.open("w", encoding="utf-8") as f:
    # ensure_ascii=False -> keep Chinese readable
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Converted {len(items)} valid items to {dst}")