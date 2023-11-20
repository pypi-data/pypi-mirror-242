from abc import ABC, abstractmethod


class _Iterator(ABC):
    @abstractmethod
    def __init__(self, file: str) -> None:
        self.file = file

    @abstractmethod
    def __iter__(self) -> "BaseIterator":
        ...

    @abstractmethod
    def __next__(self) -> str:
        ...


class BaseIterator(_Iterator):
    """
       Base class for custom iterators used in pyxreader.

       classes should inherit from this class when creating custom iterators.

       Attributes:
       - `file`: The path to the file being iterated.

       Methods:
       - `__init__(self, file: str)`: Constructor to initialize the iterator with the
          file path.
       - `__iter__(self) -> BaseIterator`: Method to initialize the iterator.
       - `__next__(self) -> str`: Method to extract the next item in the iteration.
          Raises StopIteration by default.
    """

    def __init__(self, file: str) -> None:
        super().__init__(file)

    def __iter__(self) -> "BaseIterator":
        return self

    def __next__(self) -> str:
        raise StopIteration
