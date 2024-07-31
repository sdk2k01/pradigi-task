from typing import Any
from re import sub
from llama_index.core import Document
import uuid


class DocumentTransformer:
    """
    Class implementing some useful document transformation functions.
    """

    def __init__(self, doc: Document) -> None:
        self.doc = doc

    def __call__(self) -> Any:
        self.doc = self.generate_doc_id(self.doc)

    @staticmethod
    def clean_string(text, **kwargs):
        # Remove all tab characters and any surrounding spaces
        text = sub(r"\t\s*", "", text)

        # Replace more than two consecutive newline characters (with any number of spaces in between) with exactly two newlines
        text = sub(r"\n\s*\n\s*\n+", "\n\n", text)

        # Replace multiple spaces with a single space
        text = sub(r" +", " ", text)

        # Remove spaces before newlines
        text = sub(r" \n", "\n", text)

        return text

    @staticmethod
    def generate_doc_id(doc: Document):
        """
        Generate document id as valid uuid4 string.
        """
        doc.doc_id = str(uuid.uuid4())
        return doc
