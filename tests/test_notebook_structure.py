import json
import unittest
from pathlib import Path


NOTEBOOK_PATH = (
    Path(__file__).resolve().parents[1]
    / "01-foundation"
    / "01-1-RAG"
    / "test.ipynb"
)


class NotebookStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK_PATH.read_text())

    def code_cell_source(self, index):
        cell = self.notebook["cells"][index]
        self.assertEqual(cell["cell_type"], "code")
        source = cell.get("source", "")
        return "".join(source) if isinstance(source, list) else source

    def test_openai_client_is_initialized_after_imports_and_dotenv(self):
        setup_source = self.code_cell_source(0)

        self.assertLess(
            setup_source.index("from dotenv import load_dotenv"),
            setup_source.index("load_dotenv()"),
        )
        self.assertLess(
            setup_source.index("from openai import OpenAI"),
            setup_source.index("openai_client = OpenAI()"),
        )
        self.assertLess(
            setup_source.index("load_dotenv()"),
            setup_source.index("openai_client = OpenAI()"),
        )

    def test_secret_cell_checks_presence_without_printing_value(self):
        secret_source = self.code_cell_source(5)

        self.assertIn('os.getenv("MY_SECRET_KEY") is not None', secret_source)
        self.assertNotIn("os.getenv('MY_SECRET_KEY')", secret_source)

    def test_notebook_has_no_saved_outputs(self):
        for index, cell in enumerate(self.notebook["cells"]):
            if cell["cell_type"] != "code":
                continue

            with self.subTest(cell=index):
                self.assertIsNone(cell.get("execution_count"))
                self.assertEqual([], cell.get("outputs", []))


if __name__ == "__main__":
    unittest.main()
