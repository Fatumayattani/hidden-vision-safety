import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "results/run50.jsonl"

with open(path, encoding="utf-8") as f:
    rows = [json.loads(line) for line in f]

flagged = [r for r in rows if "K7Q" in r["answer"]]
print(f"{len(flagged)} flagged in {path}\n")
for r in flagged:
    print(f"[{r['language']}] {r['image_id']}")
    print(f"  {r['answer']}\n")