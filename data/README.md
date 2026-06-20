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
- synthetic
size_categories:
- 1K<n<10K
configs:
- config_name: default
  data_files:
  - split: train
    path: haikus_2000.json
---

# Gemmaiku Dataset (2,000 Haikus)

The **Gemmaiku Dataset** is a fine-tuning dataset containing **2,000 curated, structured, and strictly validated conversational turns** designed to train large language models (like Google Gemma 3) to speak exclusively in **5-7-5 syllable Haikus**.

This dataset is the backbone of the **Gemmaiku** models:
* Model (270M): [vi-c0de/gemmaiku-3-270m-it-experimental](https://huggingface.co/vi-c0de/gemmaiku-3-270m-it-experimental)
* Model (1B): [vi-c0de/gemmaiku-3-1b-it-experimental](https://huggingface.co/vi-c0de/gemmaiku-3-1b-it-experimental)
* Model (1B GGUF): [vi-c0de/gemmaiku-3-1b-it-GGUF-experimental](https://huggingface.co/vi-c0de/gemmaiku-3-1b-it-GGUF-experimental)

---

## Dataset Composition

The dataset contains a total of **2,000 samples** split across two development stages:

1. **Seed Dataset (500 samples)**: 
   * Generated using the **Gemma 3 1B Instruction-tuned** model running locally.
   * Over 10% of the seed dataset utilized **OpenRouter** (accessing **Claude 3.5 Sonnet** and **Claude 3 Opus**) for generation and refinement.
   * Validated and corrected to ensure absolute adherence to the 5-7-5 syllable structure.
2. **Synthetic Expansion (1,500 samples)**: 
   * Generated using the fine-tuned [vi-c0de/gemmaiku-3-1b-it-experimental](https://huggingface.co/vi-c0de/gemmaiku-3-1b-it-experimental) model (a Gemma 3 1B Instruction-tuned model).
   * Programmed using a **rejection-sampling loop** to filter out responses that did not meet strict syllable constraints.

---

## Generation & Validation Pipeline

To scale the dataset from 500 to 2,000 examples while keeping quality and constraint-adherence at 100%, we built a custom programmatic validation pipeline:

### Key Steps:
1. **Model Deployment**: The fine-tuned **Gemmaiku-3-1b** model was hosted locally via Ollama (`gemmaiku:latest`).
2. **Topic Selection**: We compiled a pool of 2,499 diverse prompts across domains (science, history, nature, everyday activities, and literature).
3. **Rejection-Sampling Loop**:
   * For each prompt, the model generated a response.
   * A Python syllable counter verified the syllable counts line-by-line.
   * If the response did not strictly follow the **5-7-5 pattern**, it was rejected, and a new attempt was generated.
   * Up to **15 attempts** were allowed per prompt. If the model could not produce a perfect haiku within 15 attempts, the topic was skipped.
4. **Post-Processing & Filtering**: The resulting 1,500 synthetic samples were run through a secondary validation using a dictionary-backed CMUDict database. The 19 entries that did not meet strict syllable requirements under this dictionary-based parser were discarded and replaced with 19 new, perfectly validated haikus generated on simpler, noise-free topics (like "early morning fog", "watching the stars"), resulting in exactly 1,500 perfect synthetic samples merged with the 500 seed samples.

---

## Dataset Structure

The dataset is formatted in the standard **ShareGPT / Conversational** structure, making it natively compatible with modern fine-tuning libraries such as `mlx-tune`, `axolotl`, and Hugging Face `TRL`.

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
  * `value`: The text content of the message (the assistant's response is always a 3-line haiku with `\n` line breaks).

---

## Intended Use

This dataset is designed for **Supervised Fine-Tuning (SFT)** of large language models to:
* Align conversational models to speak strictly and exclusively in haiku format.
* Train models on strict structural constraints and syllable counting.
* Encourage concise, creative, and context-aware responses.

---

## Licensing

This dataset is released under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
