.PHONY: setup ingest api ui test
setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
ingest:
	python -m src.ingest --input_dir data/raw --persist_dir data/vectorstore
api:
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
ui:
	streamlit run src/ui_streamlit.py
test:
	pytest -q
