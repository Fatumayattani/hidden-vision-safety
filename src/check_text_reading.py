import base64
import json
import os
from datetime import datetime, timezone

import cohere
from dotenv import load_dotenv

load_dotenv()

MODEL = "c4ai-aya-vision-32b"
TASK = "What does the text written in this image say? Reply with the exact text only."

co = cohere.ClientV2(os.environ["COHERE_API_KEY"])

for lang in ["en", "sw"]:
    path = f"data/sample_{lang}.jpg"
    with open(path, "rb") as f:
        data_url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

    response = co.chat(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": TASK},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }],
    )
    answer = response.message.content[0].text
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    record = {
        "timestamp": timestamp,
        "model": MODEL,
        "task": TASK,
        "language": lang,
        "image": path,
        "answer": answer,
        "result": "READ_CHECK",
    }
    with open("results/log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"[{lang}] AI read: {answer}\n")