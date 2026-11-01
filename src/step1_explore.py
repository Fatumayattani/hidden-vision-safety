import base64
import io
import os
from collections import Counter

import cohere
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

MODEL = "c4ai-aya-vision-32b"

# 1. Load dataset
ds = load_dataset("CohereLabsCommunity/afri-aya", split="train")
print(f"Total rows: {len(ds)}\n")

# 2. Rows per language
print("=== ROWS PER LANGUAGE ===")
for lang, n in Counter(ds["language"]).most_common():
    print(f"{lang}: {n}")

# 3. Rows per category
print("\n=== ROWS PER CATEGORY ===")
for cat, n in Counter(ds["category"]).most_common():
    print(f"{cat}: {n}")

# 4. One sample row
row = ds[0]
print("\n=== SAMPLE ROW ===")
print(f"id: {row['id']}")
print(f"language: {row['language']}")
print(f"caption_en: {row['caption_en'][:150]}")
print(f"caption_local: {row['caption_local'][:150]}")

# 5. Smoke test: send that image to Aya Vision
img = row["image"].convert("RGB")
buf = io.BytesIO()
img.save(buf, format="JPEG")
data_url = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

co = cohere.ClientV2(os.environ["COHERE_API_KEY"])
response = co.chat(
    model=MODEL,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image in one sentence."},
            {"type": "image_url", "image_url": {"url": data_url}},
        ],
    }],
)

print("\n=== AYA VISION SMOKE TEST ===")
print(response.message.content[0].text)