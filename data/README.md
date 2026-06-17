---
license: apache-2.0
task_categories:
- text-generation
language:
- en
tags:
- haiku
- gemma
- gemma-3
- mlx
- mlx-tune
- conversational
- sharegpt
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: train
    path: haikus_dataset.json
---

# Gemmaiku Dataset

A fine-tuning dataset containing 500 curated, structured, and strictly validated conversational turns designed to train models (like Gemma 3) to speak exclusively in **5-7-5 syllable Haikus**.

This dataset is the backbone of the **Gemmaiku** models:
* [vi-c0de/gemmaiku-3-270m-it-experimental](https://huggingface.co/vi-c0de/gemmaiku-3-270m-it-experimental)
* [vi-c0de/gemmaiku-3-1b-it-experimental](https://huggingface.co/vi-c0de/gemmaiku-3-1b-it-experimental)

---

## Dataset Structure

The dataset is formatted in the standard **ShareGPT / Conversational** style, making it compatible with modern fine-tuning libraries like `mlx-tune`, `axolotl`, and `TRL`.

### Example Entry

```json
{
  "conversations": [
    {
      "from": "human",
      "value": "What is the capital of France?"
    },
    {
      "from": "gpt",
      "value": "Paris holds the key,\nCity of lights, grand and bright,\nCapital stands proud."
    }
  ]
}
```

### Data Fields

* `conversations`: A list of messages representing a single conversation thread.
  * `from`: The sender of the message (`human` / `gpt`).
  * `value`: The text content of the message.

---

## Validation & Quality Control

To ensure high-quality fine-tuning, every single response in this dataset went through a validation pipeline:
1. **Syllable Counting**: Responses were split into lines and evaluated using the `syllables` Python library.
2. **Strict 5-7-5 Matching**: Any response that did not strictly contain exactly 5 syllables in the first line, 7 in the second, and 5 in the third was flagged.
3. **Manual & LLM Curation**: All flagged entries were corrected and re-verified to guarantee a 100% perfect haiku rate.

---

## Intended Use

This dataset is designed for supervised fine-tuning (SFT) of instruction-tuned large language models, specifically:
* Aligning models to speak strictly in haikus.
