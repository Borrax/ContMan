import uuid
from abc import abstractmethod, ABCMeta


class BaseItem(metaclass=ABCMeta):
    year = None
    title = None
    creator = None
    id = None

    @abstractmethod
    def __init__(self, year, title, creator):
        self.year = year
        self.title = title
        self.creator = creator
        self.id = uuid.uuid4()


class Book(BaseItem):
    def __init__(self, year, title, creator):
        super().__init__(year, title, creator)


class Game(BaseItem):
    def __init__(self, year, title, creator):
        super().__init__(year, title, creator)


class Movie(BaseItem):
    def __init__(self, year, title, creator):
        super().__init__(year, title, creator)
