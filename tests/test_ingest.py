from pathlib import Path
from src.ingest import main

def test_ingest_runs(tmp_path: Path):
    d = tmp_path / "raw"
    d.mkdir()
    csv = d / "teachers.csv"
    csv.write_text("subject,teacher\nOB,Dr. Rao\nEconomics,Prof. Sen\n")
    out = tmp_path / "index"
    main(str(d), str(out))
    assert out.exists() and any(out.iterdir())
