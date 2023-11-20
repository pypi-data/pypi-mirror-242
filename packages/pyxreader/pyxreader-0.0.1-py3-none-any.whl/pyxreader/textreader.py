import pyttsx3

from typing import Optional
from pyxreader._defaults import Default


class TextReader:
    engine: pyttsx3.Engine

    def __init__(
        self,
        content: Optional[str] = None,
        *,
        voice: str = Default.voice,
        reading_spead: int = Default.speed,
        volume: float = Default.volume,
    ) -> None:
        """
        Initialize an object for text-to-speech conversion.
        """
        self.content: str | None = content
        self.engine: pyttsx3.Engine = pyttsx3.init()
        if voice:
            self.engine.setProperty("voice", voice)
        self.engine.setProperty("rate", reading_spead)
        self.engine.setProperty("volume", volume)

    def execute(self) -> "TextReader":
        """
        Execute the text-to-speech engine to vocalize the provided content.

        :return: The modified TextReader object after execution.
        """
        self.engine.runAndWait()
        return self

    def say(self, content: Optional[str] = None) -> "TextReader":
        """
        Add text content to the TextReader's queue to be spoken.

        :param content: The text content to be spoken. If None, uses the content
                       provided during initialization.
        :return: The modified Speaker object after queuing the content.
        """
        if content:
            self.engine.say(content)
        else:
            self.engine.say(self.content)
        return self

    def save(self, filename: Optional[str] = None) -> "TextReader":
        """
        Save the spoken content to an audio file.

        :param filename: The name of the file to save the spoken content to.
        :return: The modified TextReader object after saving to a file.
        """
        if filename:
            self.engine.save_to_file(text=self.content, filename=filename)
        return self

    def read_file(self, filename: Optional[str] = None) -> "TextReader":
        """
        Read the content of a file line by line and vocalize each line.

        :param filename: The path to the file to be read and spoken.
        :return: The modified object after reading and vocalizing the file.
        """
        if filename:
            with open(filename) as f:
                for line in f:
                    self.say(line)
        return self
