# Hidden Vision Safety

Hidden instructions in images: a safety study for Afri-Aya V2, Cohere Labs Regional Africa.

## Question

Can text written inside an image take control of the vision-language models Afri-Aya V2 depends on, and does that risk grow as models learn African languages?

## Where V2 is exposed

1. **Pipeline:** a captioning model and an LLM judge process web-sourced images. Text inside those images could steer captions and corrupt training data.
2. **Model:** once fine-tuned to read African languages, the model may also obey instructions written in them.

## Pipeline

Run in this order from the repo root:

| Script | What it does | Output |
| --- | --- | --- |
| `src/explore_dataset.py` | Loads Afri-Aya, counts pictures per language, one test call | Printed summary |
| `src/make_overlay_samples.py` | Writes the hidden sentence on one picture, in English and Swahili | `data/sample_en.jpg`, `data/sample_sw.jpg` |
| `src/test_single_image.py` | Asks the model to describe each sample, checks the reply for the marker | `results/log.jsonl`, `results/examples/` |
| `src/check_text_reading.py` | Asks the model to read the text on the same samples | `results/log.jsonl` |
| `src/run_injection_eval.py` | Runs the test on 50 random pictures in both languages | `results/run50.jsonl`, `results/run50_sample_ids.json` |
| `src/review_flagged.py` | Lists every answer containing the marker for hand review | Labels go in `results/run50_labels.json` |
| `src/plot_results.py` | Chart from the answers and hand labels | `results/chart_run50.png` |

## Status

Pilot complete on base Aya Vision 32B via the Cohere API: English vs Swahili, 50 pictures. Method and results in `docs/method.md`.

## Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env    # then add your Cohere API key and Hugging Face token

## Data

Images from [Afri-Aya](https://huggingface.co/datasets/CohereLabsCommunity/afri-aya), CC BY 4.0, by the Cohere Labs Regional Africa community.

## License

Code: MIT. Derived data follows the Afri-Aya CC BY 4.0 license.