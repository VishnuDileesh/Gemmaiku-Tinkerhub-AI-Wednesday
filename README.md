# AI-Wednesday-Gemmaiku

Fine-tuning Gemma models on Apple Silicon using MLX.

## Project Structure

```text
├── data/
│   ├── raw/                  # Original raw datasets (e.g. haikus.json)
│   └── processed/            # Processed datasets ready for fine-tuning
├── models/                   # Local model weights, configs, and adapters 
├── notebooks/
│   ├── data_preparation/     # Dataset exploration, analysis, and preparation
│   ├── gemma_3_270m/         # Gemma-3 270M fine-tuning and inference
│   └── gemma_3_1b/           # Gemma-3 1B fine-tuning and inference
├── src/
│   └── gemmaiku/             # Shared reusable Python code (local package)
├── pyproject.toml            # Project configuration and dependency definitions
└── uv.lock                   # Pinned dependency lockfile
```

## Setup & Installation

This project uses `uv` for Python package and virtual environment management.

1. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Sync the project dependencies:
   ```bash
   uv sync
   ```
   *Note: This automatically installs the helper package `src/gemmaiku` in editable mode.*

## Running the Notebooks

### In VS Code
1. Open the project folder in VS Code.
2. Open any `.ipynb` notebook inside the `notebooks/` directory.
3. Select the Jupyter Kernel pointing to the `.venv` directory created by `uv` in the project root.

### In Terminal
To start a Jupyter session using the project environment:
```bash
uv run --with jupyter jupyter lab
```

## Reusable Modules
You can import helper code (like the syllable counter) anywhere in the project or notebooks:
```python
from gemmaiku import get_syllable_count_for_line
```
