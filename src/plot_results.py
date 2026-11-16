import json
from collections import Counter

import matplotlib.pyplot as plt

RUNS = [
    ("Run 1\n50 pictures", "results/run50.jsonl", "results/run50_labels.json"),
    ("Run 2 (repeat)\nsame 50", "results/run50_repeat.jsonl", "results/run50_repeat_labels.json"),
    ("Run 3\n100 new pictures", "results/run100.jsonl", "results/run100_labels.json"),
]
TOOK_CONTROL = {"OBEYED", "PARTIAL", "HIJACKED"}
GROUP = {
    "OBEYED": "Taken over",
    "PARTIAL": "Taken over",
    "HIJACKED": "Taken over",
    "QUOTED": "Quoted the text",
    "IGNORED": "Ignored the text",
}


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def load_labels(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["labels"]


def wilson(k, n, z=1.96):
    """95% range for a rate of k out of n."""
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, c - h), min(1.0, c + h)


# ---------- Chart 1: run 1 breakdown (used in the slides) ----------
rows = load_jsonl("results/run50.jsonl")
labels = load_labels("results/run50_labels.json")
counts = {"en": Counter(), "sw": Counter()}
for r in rows:
    label = labels.get(f"{r['image_id']}|{r['language']}", {}).get("label", "IGNORED")
    counts[r["language"]][GROUP[label]] += 1

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
plt.close(fig)
print("Saved results/chart_run50.png")

# ---------- Chart 2: took control, all runs ----------
summary = []
for name, log_path, labels_path in RUNS:
    rows = load_jsonl(log_path)
    labels = load_labels(labels_path)
    total = Counter(r["language"] for r in rows)
    took = Counter(k.split("|")[1] for k, v in labels.items() if v["label"] in TOOK_CONTROL)
    for lang in ["en", "sw"]:
        k, n = took[lang], total[lang]
        lo, hi = wilson(k, n)
        summary.append((name, lang, k, n, k / n, lo, hi))

print("\n=== TOOK CONTROL ===")
for name, lang, k, n, rate, lo, hi in summary:
    print(f"{name.splitlines()[0]:<15} {names[lang]:<8} {k:>3} of {n:<4} {rate:>5.0%}  (likely {lo:.0%} to {hi:.0%})")

fig, ax = plt.subplots(figsize=(8, 3.6))
run_names = [r[0] for r in RUNS]
w = 0.36
for j, (lang, color) in enumerate([("en", "#1F5F7A"), ("sw", "#8fb3d9")]):
    pts = [s for s in summary if s[1] == lang]
    xs = [i + (j - 0.5) * w for i in range(len(pts))]
    rates = [s[4] * 100 for s in pts]
    err_lo = [(s[4] - s[5]) * 100 for s in pts]
    err_hi = [(s[6] - s[4]) * 100 for s in pts]
    bars = ax.bar(xs, rates, w, color=color, label=names[lang],
                  yerr=[err_lo, err_hi], capsize=4, error_kw={"elinewidth": 1, "ecolor": "#555555"})
    for x, s in zip(xs, pts):
        ax.text(x, -2.2, f"{s[2]}/{s[3]}", ha="center", va="top", fontsize=9, color="#333333")
ax.set_xticks(range(len(run_names)))
ax.set_xticklabels(run_names, fontsize=10)
ax.tick_params(axis="x", pad=16)
ax.set_ylabel("Took control (%)")
ax.set_ylim(0, 25)
ax.set_title("Took control, by run and language (lines show the likely range)", loc="left", fontsize=12)
ax.legend(frameon=False)
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
plt.tight_layout()
plt.savefig("results/chart_all_runs.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("\nSaved results/chart_all_runs.png")