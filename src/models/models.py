import uuid
from abc import abstractmethod, ABCMeta


class BaseItem(metaclass=ABCMeta):
    year = None
    title = None
    cover = None
    id = None

    @abstractmethod
    def __init__(self, year, title, cover=None):
        self.year = year
        self.title = title
        self.cover = cover
        self.id = uuid.uuid4()


class Book(BaseItem):
    def __init__(self, year, title):
        super().__init__(year, title)


class Game(BaseItem):
    def __init__(self, year, title):
        super().__init__(year, title)


class Movie(BaseItem):
    def __init__(self, year, title, cover, duration='N/A'):
        super().__init__(year, title, cover)
        self.duration = duration
