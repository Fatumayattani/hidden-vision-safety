import json
from collections import Counter

import matplotlib.pyplot as plt

# 1. Load run results and hand labels
with open("results/run50.jsonl", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f]

with open("results/run50_labels.json", encoding="utf-8") as f:
    labels = json.load(f)["labels"]

# 2. Final label per answer: hand label if reviewed, otherwise IGNORED
GROUP = {
    "OBEYED": "Taken over",
    "PARTIAL": "Taken over",
    "HIJACKED": "Taken over",
    "QUOTED": "Quoted the text",
    "IGNORED": "Ignored the text",
}
counts = {"en": Counter(), "sw": Counter()}
for r in rows:
    key = f"{r['image_id']}|{r['language']}"
    label = labels.get(key, {}).get("label", "IGNORED")
    counts[r["language"]][GROUP[label]] += 1

# 3. Print the numbers
for lang, c in counts.items():
    print(lang, dict(c), "total", sum(c.values()))

# 4. Horizontal stacked bars
names = {"en": "English", "sw": "Swahili"}
order = ["Ignored the text", "Quoted the text", "Taken over"]
colors = ["#d9d9d9", "#8fb3d9", "#c0392b"]

fig, ax = plt.subplots(figsize=(8, 2.8))
langs = ["sw", "en"]
for lang_i, lang in enumerate(langs):
    left = 0
    for cat, color in zip(order, colors):
        n = counts[lang][cat]
        ax.barh(lang_i, n, left=left, color=color, edgecolor="white",
                label=cat if lang_i == 0 else None)
        if n:
            ax.text(left + n / 2, lang_i, str(n), ha="center", va="center", fontsize=10)
        left += n

ax.set_yticks(range(len(langs)))
ax.set_yticklabels([names[l] for l in langs])
ax.set_xlabel("Images (out of 50)")
ax.set_xlim(0, 50)
ax.set_title("Hidden instruction in the image: what Aya Vision did", loc="left")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=3, frameon=False)
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)

plt.tight_layout()
plt.savefig("results/chart_run50.png", dpi=200, bbox_inches="tight")
print("Saved results/chart_run50.png")