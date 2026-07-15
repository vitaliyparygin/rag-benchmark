# Installation

## Requirements

* Python 3.10+
* pip
* virtual environment (recommended)

## Install from source

```bash
git clone https://github.com/<username>/rag-benchmark.git

cd rag-benchmark

python -m venv .venv

source .venv/bin/activate

pip install -e .
```

Development installation:

```bash
pip install -e ".[dev]"
```

LLM support:

```bash
pip install -e ".[llm]"
```

Everything:

```bash
pip install -e ".[dev,llm]"
```

## Verify installation

```bash
rag-benchmark --help
```

You should see the list of available CLI commands.

## Upgrade

```bash
git pull

pip install -e .
```

## Running tests

```bash
pytest
```

## Formatting

```bash
ruff format .
```

## Linting

```bash
ruff check .
```
