import json
import unittest
from pathlib import Path


NOTEBOOK = Path(__file__).resolve().parents[1] / "01-foundation" / "01-1-RAG" / "test.ipynb"


def _code_cells():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    return [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]


def _source(cell):
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


class NotebookSetupTest(unittest.TestCase):
    def test_notebook_initializes_openai_after_imports_and_dotenv(self):
        non_empty_sources = [_source(cell) for cell in _code_cells() if _source(cell).strip()]
        setup_source = non_empty_sources[0]

        self.assertLess(
            setup_source.index("from dotenv import load_dotenv"),
            setup_source.index("load_dotenv()"),
        )
        self.assertLess(setup_source.index("from openai import OpenAI"), setup_source.index("OpenAI()"))
        self.assertLess(setup_source.index("load_dotenv()"), setup_source.index("OpenAI()"))

    def test_notebook_does_not_commit_execution_outputs(self):
        for cell in _code_cells():
            self.assertIsNone(cell.get("execution_count"))
            self.assertEqual(cell.get("outputs"), [])

    def test_notebook_does_not_display_secret_values(self):
        sources = [_source(cell) for cell in _code_cells()]

        self.assertIn('os.getenv("MY_SECRET_KEY") is not None', sources)
        self.assertNotIn("os.getenv('MY_SECRET_KEY')", sources)
