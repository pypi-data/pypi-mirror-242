"""
pyxreader

The `pyxreader` module provides utilities for reading and vocalizing text content from various file formats.
"""
from pyxreader.textreader import TextReader
from .iterators.pdf_iterator import BaseIterator, PDFTextIterator
from  pyxreader.adaptable import AdaptableReader

