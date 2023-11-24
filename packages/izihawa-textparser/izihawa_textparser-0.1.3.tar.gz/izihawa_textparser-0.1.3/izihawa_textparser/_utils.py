import re


class ProcessedDocument:
    def __init__(self, processed_document):
        self.processed_document = processed_document

    @staticmethod
    async def setup(file_data, grobid_client):
        return ProcessedDocument(
            await grobid_client.process_fulltext_document(pdf_file=file_data)
        )

    @property
    def doi(self):
        return self.processed_document.get("doi")

    @property
    def title(self):
        return self.processed_document.get("title")

    @property
    def abstract(self):
        return self.processed_document.get("abstract")

    @property
    def body(self):
        return self.processed_document.get("body")


BANNED_SECTIONS = {
    "author contribution",
    "data availability statement",
    "declaration of competing interest",
    "acknowledgments",
    "acknowledgements",
    "supporting information",
    "conflict of interest disclosures",
    "conflict of interest",
    "conflict of interest statement",
    "ethics statement",
    "references",
    "external links",
    "further reading",
    "works cited",
    "bibliography",
    "notes",
    "sources",
    "footnotes",
    "suggested readings",
}


def clean_empty_references(text: str):
    text = re.sub(r"\((?:[Ff]ig|[Tt]able|[Ss]ection)\.?\s*[^)]*\)", "", text)
    text = re.sub(r"\[[,\s–\d]*]", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+([.,;])", "\g<1>", text, flags=re.MULTILINE)
    return text
