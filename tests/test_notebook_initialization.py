import json
import unittest
from pathlib import Path


NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "01-foundation" / "01-1-RAG" / "test.ipynb"


class NotebookInitializationTests(unittest.TestCase):
    def test_openai_client_is_created_after_imports_and_dotenv_load(self):
        notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        first_code_cell = next(
            cell for cell in notebook["cells"] if cell.get("cell_type") == "code" and cell.get("source")
        )
        source = "".join(first_code_cell["source"])

        openai_import_index = source.find("from openai import OpenAI")
        dotenv_import_index = source.find("from dotenv import load_dotenv")
        dotenv_load_index = source.find('load_dotenv(".env")')
        client_init_index = source.find("openai_client = OpenAI()")

        self.assertNotEqual(openai_import_index, -1)
        self.assertNotEqual(dotenv_import_index, -1)
        self.assertNotEqual(dotenv_load_index, -1)
        self.assertNotEqual(client_init_index, -1)
        self.assertLess(openai_import_index, client_init_index)
        self.assertLess(dotenv_import_index, dotenv_load_index)
        self.assertLess(dotenv_load_index, client_init_index)


if __name__ == "__main__":
    unittest.main()
