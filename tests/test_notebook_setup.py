import json
from pathlib import Path


NOTEBOOK = Path(__file__).resolve().parents[1] / "01-foundation" / "01-1-RAG" / "test.ipynb"


def _code_cells():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    return [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]


def _source(cell):
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def test_notebook_initializes_openai_after_imports_and_dotenv():
    non_empty_sources = [_source(cell) for cell in _code_cells() if _source(cell).strip()]
    setup_source = non_empty_sources[0]

    assert setup_source.index("from dotenv import load_dotenv") < setup_source.index("load_dotenv()")
    assert setup_source.index("from openai import OpenAI") < setup_source.index("OpenAI()")
    assert setup_source.index("load_dotenv()") < setup_source.index("OpenAI()")


def test_notebook_does_not_commit_execution_outputs():
    for cell in _code_cells():
        assert cell.get("execution_count") is None
        assert cell.get("outputs") == []


def test_notebook_does_not_display_secret_values():
    sources = [_source(cell) for cell in _code_cells()]

    assert 'os.getenv("MY_SECRET_KEY") is not None' in sources
    assert "os.getenv('MY_SECRET_KEY')" not in sources
