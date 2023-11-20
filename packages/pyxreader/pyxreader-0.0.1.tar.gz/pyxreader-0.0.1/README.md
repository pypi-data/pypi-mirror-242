# pyxreader

pyxreader is a Python module that streamlines the process of reading and vocalizing the content of  files using text-to-speech capabilities in a memory-efficient way. It provides a flexible and extensible architecture to support various file formats and allows for custom methods that the user can choose to extract text from various files.

## Features

- Read and vocalize the content of any file.
- Easily configure reading speed, volume, and voice.
- Support for custom dependency injection, enabling users to define their own text extraction logic for various file formats. The module comes with native support for PDFs.

## Installation

```bash
pip install pyxreader
```
if you're on linux, for the speech capabilities you might also need to install:
```bash
sudo apt update && sudo apt install espeak ffmpeg libespeak1
```
> **Note:** The text-to-speech capabilities are provided by **[pyttsx3](https://github.com/nateshmbhat/pyttsx3)**. If you encounter any issues with speech not functioning on your system, make sure to consult the library for more information.

# Configuration
The Reader class allows you to configure various settings:

- speed: Reading speed in words per minute (default: 200).
- volume: Volume level, a float between 0.0 and 1.0 (default: 1.0).
- voice: The voice to use for reading (default: operating system).

# Usage


## Normal text file reader

````python
from pyxreader import TextReader

# Speak the provided text
TextReader("Hey there!").say().execute()

# Save spoken text to an MP3 file
TextReader("Whatever it read").save("output.mp3").execute()

# Read and speak the content of a normal file line by line
TextReader().read_file("reader.py").execute()
````

## Custom files (PDFs by default)

````python
from pyxreader import AdaptableReader

# Read and vocalize the content of a PDF file with default settings
# Defaults to the base iterator PDFTextIterator.
AdaptableReader(filename="example.pdf").read()
````

#### This uses `PDFTextIterator` to parse PDFs and extract text per page

#### How it works
````python
from pyxreader import PDFTextIterator


per_page = PDFTextIterator("any.pdf")
for line in per_page:
    print(line)
````

#### If the file you have is not a PDF like

````python
AdaptableReader(filename="example.custom").read()
````
#### Then define your own custom file iterator

````python
from pyxreader import AdaptableReader
from pyxreader.iterators import BaseIterator


class CustomIterator(BaseIterator):
    def __init__(self, file: str):
        super().__init__(file)
        # Additional initialization for your custom iterator

    def __iter__(self) -> "CustomIterator":
        """
        Method to initialize the custom iterator.
        """
        pass

    def __next__(self) -> str:
        """
        Method to extract the next item in the iteration.
        """
        # Implement the logic to extract the next item in the iteration for your custom iterator
        # This method should return a string
        pass


# Example using a custom iterator
AdaptableReader("example.custom").inject_iterator(CustomIterator).read()
````
