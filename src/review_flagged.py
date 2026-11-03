import json

with open("results/run50.jsonl", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f]

obeyed = [r for r in rows if r["result"] == "OBEYED"]
print(f"{len(obeyed)} obeyed\n")
for r in obeyed:
    print(f"[{r['language']}] {r['image_id']}  ({r['image']})")
    print(f"  {r['answer']}\n")