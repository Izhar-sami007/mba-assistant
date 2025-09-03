#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt
python -m src.ingest --input_dir data/raw --persist_dir data/vectorstore
uvicorn src.app:app --host 0.0.0.0 --port 8000
