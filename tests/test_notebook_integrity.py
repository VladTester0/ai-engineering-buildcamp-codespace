import json
import unittest
from pathlib import Path


NOTEBOOK_PATH = Path("01-foundation/01-1-RAG/test.ipynb")


def _code_sources():
    notebook = json.loads(NOTEBOOK_PATH.read_text())
    return [
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]


class NotebookIntegrityTest(unittest.TestCase):
    def test_openai_client_is_initialized_after_setup(self):
        source = "\n".join(_code_sources())

        dotenv_import = source.index("from dotenv import load_dotenv")
        openai_import = source.index("from openai import OpenAI")
        dotenv_load = source.index("load_dotenv()")
        client_init = source.index("openai_client = OpenAI()")

        self.assertLess(dotenv_import, dotenv_load)
        self.assertLess(dotenv_load, client_init)
        self.assertLess(openai_import, client_init)


if __name__ == "__main__":
    unittest.main()
