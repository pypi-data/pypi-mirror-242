import pypdf

from typing import BinaryIO
from pyxreader.iterators.base import BaseIterator

class PDFTextIterator(BaseIterator):
    def __init__(self, pdf_file: str) -> None:
        """
        A base iterator for extracting text content from PDF files.

        This here allows you to iterate through the pages of a PDF file and extract
        the text content from each page.

        Args:
            pdf_file (str): The path to the PDF file.
            This will be chosen by the Reader class.

        Attributes:
            pdf (BinaryIO | None): The binary file object representing the PDF file.
            reader (pypdf.PdfReader | None): The PDF reader object for accessing
            the PDF content.
            page_index (int): The current index of the page being processed.

        Methods:
            __iter__(): Initialize the iterator,
            by opening the PDF file and setting up the PDF reader object.
            __next__(): Extract the text content of the next page in the PDF.

        Raises:
            StopIteration: Raised when there are no more pages to iterate.

        Example:
            ```python
            iterator = PDFTextIterator("example.pdf")
            for text_content in iterator:
                print(text_content)
            ```
        """
        super().__init__(pdf_file)
        self.pdf: BinaryIO | None = None
        self.reader: pypdf.PdfReader | None = None
        self.page_index: int = 0

    def __iter__(self) -> "PDFTextIterator":
        """
        Initialize the iterator by opening the PDF file and setting up the PDF reader.
        Returns:
           PDFTextIterator: The PDFTextIterator object.
        """
        self.pdf = open(self.file, "rb")
        self.reader = pypdf.PdfReader(self.pdf, strict=False)
        self.page_index = 0
        return self

    def __next__(self) -> str:
        """
        Extracts the text content of the next page in the PDF.

        Returns:
           str: The extracted text content as a string.

        Raises:
           StopIteration: Raised when there are no more pages to iterate over.
        """
        if self.page_index < len(self.reader.pages):
            content = self.reader.pages[self.page_index].extract_text()
            self.page_index += 1
            return content
        else:
            self.pdf.close()
            raise StopIteration
