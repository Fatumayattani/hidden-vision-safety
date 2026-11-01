# Hidden Vision Safety

Hidden instructions in images: a safety study for Afri-Aya V2, Cohere Labs Regional Africa.

## Question

Can text written inside an image take control of the vision-language models Afri-Aya V2 depends on, and does that risk grow as models learn African languages?

## Where V2 is exposed

1. **Pipeline:** a captioning model and an LLM judge process web-sourced images. Text inside those images could steer captions and corrupt training data.
2. **Model:** once fine-tuned to read African languages, the model may also obey instructions written in them.

## Approach

Each image is tested clean and with text overlaid, under the same neutral task a captioner gets:

| Condition | Overlaid text | What it isolates |
| --- | --- | --- |
| Clean | None | Normal behaviour |
| Read | The image's own local-language caption | Can the model read the language? |
| Inject, English | Off-task instruction in English | English baseline |
| Inject, local | The same instruction, translated by a native speaker | Does it obey the African language? |

Results are reported per language.

## Status

Pilot in progress on base Aya Vision 32B via the Cohere API.

## Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env    # then add your Cohere API key

## Data

Images from [Afri-Aya](https://huggingface.co/datasets/CohereLabsCommunity/afri-aya), CC BY 4.0, by the Cohere Labs Regional Africa community.

## License

Code: MIT. Derived data follows the Afri-Aya CC BY 4.0 license.