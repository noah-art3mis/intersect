from pypdf import PdfReader
from typing import IO, Any

# https://pypi.org/project/pypdf/
# https://pypi.org/project/pypdfium2/


def get_text_from_pdf(data: IO[Any]) -> str:
    reader = PdfReader(data)
    print(f"Read pdf. Number of pages: {len(reader.pages)}")

    # result = reader.pages[0].extract_text()

    result = ""
    for page in reader.pages:
        text = page.extract_text()
        result += text
        result += "\n\n"

    return result
