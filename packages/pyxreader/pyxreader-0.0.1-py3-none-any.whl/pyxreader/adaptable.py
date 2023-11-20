from pyxreader.textreader import TextReader
from pyxreader.iterators import BaseIterator, PDFTextIterator
from pyxreader._defaults import Default
from typing import Type


class AdaptableReader:
    def __init__(
        self,
        filename: str,
        *,
        speed: int = Default.speed,
        volume: float = Default.volume,
        voice: str = Default.voice
    ):
        """
        Initialize an object with configurable settings for text-to-speech.

        :param filename: The path to the file to be read.
        :param speed: Reading speed in words per minute range in [1..500].
        :param volume: Volume level, a float between 0.0 and 1.0
        :param voice: The voice to use for reading (defaults to the host's OS).
        """
        self.filename: str = filename
        self.speed: int = speed
        self.volume: float = volume
        self.voice: str = voice
        self.iterator: Type[BaseIterator] = PDFTextIterator

    def read(self) -> "AdaptableReader":
        """
        Reads and vocalizes the lines from each page of the given file.
        By default, the reader assumes the file is in PDF format, so, it uses
        the default PDFtextIterator.
        If you create a custom iterator, make sure you inherit from BaseIterator
        and define your own logic for the type of file you need.
        The function uses the configured settings for reading speed, volume
        and voice.

        :return: the modified AdaptableReader object.
        """

        each_page = self.iterator(self.filename)
        for line in each_page:
            (
                TextReader(
                    volume=self.volume, voice=self.voice, reading_spead=self.speed
                )
                .say(line)
                .execute()
            )
        return self

    def inject_iterator(
        self, iterator: Type[BaseIterator] = PDFTextIterator
    ) -> "AdaptableReader":
        """
        Use this method for dependency injection to set up your custom
        iterator for any type of file.
        The current PDF iterator extracts text from PDFs and returns a string
        object from each page. You can design your own custom iterator.

        :param iterator: BaseIterator object.
        :return: This method returns the modified Reader object.
        """
        self.iterator = iterator
        return self
