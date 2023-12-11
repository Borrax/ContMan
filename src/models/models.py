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
        self.id = str(uuid.uuid4())

    @abstractmethod
    def get_info(self):
        pass


class Book(BaseItem):
    def __init__(self, title, year, author, genre, cover):
        super().__init__(year, title, cover)
        self.author = author
        self.genre = genre

    def get_info(self):
        return {
            'title': self.title,
            'year': self.year,
            'author': self.author,
            'genre': self.genre,
            'cover': self.cover
        }


class Game(BaseItem):
    def __init__(self, title, year, genre, cover):
        super().__init__(year, title, cover)
        self.genre = genre

    def get_info(self):
        return {
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'cover': self.cover
        }


class Movie(BaseItem):
    def __init__(self, year, title, cover, duration):
        super().__init__(year, title, cover)
        self.duration = duration

    def get_info(self):
        return {
            'title': self.title,
            'year': self.year,
            'duration': self.duration,
            'cover': self.cover
        }
