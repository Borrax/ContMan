import os
from abc import abstractmethod, ABC
from typing import Union

from config import ROOT_DIR
from db_provider import DbProvider
from models.models import Movie, Book, Game
from utils.decorators import tryexceptwrap_builder

type ControllerMethodOutput = Union[FulfilledReq, FailedReq]


class FulfilledReq:
    def __init__(self, payload=None):
        self.payload = payload


class FailedReq:
    def __init__(self, err_msg=None):
        self.err_msg = err_msg


class BaseController(ABC):
    __db_provider = None
    __target_collection = None
    __tryexceptwrap = tryexceptwrap_builder(
        lambda e: FailedReq(e)
    )
    __default_pic = None

    @abstractmethod
    def __init__(self, db_provider: DbProvider, target_collection: str):
        self.__db_provider = db_provider
        self.__target_collection = target_collection

    @__tryexceptwrap
    def get_collection(self) -> ControllerMethodOutput:
        collection = (self.__db_provider.get_db_json()
                      .get(self.__target_collection))

        for item in collection.values():
            image_path = item.get('cover')
            item['cover'] = os.path.join(ROOT_DIR, image_path)

        return FulfilledReq(collection)

    @__tryexceptwrap
    def add_item(self, item) -> ControllerMethodOutput:
        db_json = self.__db_provider.get_db_json()
        db_json[self.__target_collection][item.id] = item.get_info()
        self.__db_provider.rewrite_db(db_json)
        return FulfilledReq()

    @__tryexceptwrap
    def delete_item(self, id) -> ControllerMethodOutput:
        db_json = self.__db_provider.get_db_json()
        del db_json[self.__target_collection][id]
        self.__db_provider.rewrite_db(db_json)
        return FulfilledReq()

    @__tryexceptwrap
    def edit_item(self, id, new_item_info) -> ControllerMethodOutput:
        db_json = self.__db_provider.get_db_json()
        if db_json[self.__target_collection].get(id) is None:
            return FailedReq('Not existing id of the item')

        db_json[self.__target_collection][id] = new_item_info
        self.__db_provider.rewrite_db(db_json)
        return FulfilledReq()

    @__tryexceptwrap
    def search_items(self, substr):
        substr = substr.lower()
        db_json = self.__db_provider.get_db_json()
        collection = db_json[self.__target_collection]
        found_items = {}

        for (id, item_info) in collection.items():
            if substr in item_info.get('title').lower():
                found_items[id] = item_info

        return FulfilledReq(payload=found_items)


class GamesController(BaseController):
    def __init__(self, db_provider):
        super().__init__(db_provider, 'games')
        self.__default_pic = os.path.join(
            ROOT_DIR, './assets/default_game.png'
        )


class BooksController(BaseController):
    def __init__(self, db_provider):
        super().__init__(db_provider, 'books')
        self.__default_pic = os.path.join(
            ROOT_DIR, './assets/default_book.png'
        )

    def add_item(self, title, year, author, genre, cover):
        if title is None or title == '':
            return FailedReq('Missing title')

        if author is None or author == '':
            author = 'N/A'

        if year is None or year == '':
            year = 'N/A'

        if genre is None or genre == '':
            genre = 'N/A'

        if cover is None or cover == '':
            cover = self.__default_pic

        new_book = Book(title, year, author, genre, cover)
        return super().add_item(new_book)

    def edit_item(self, id, item_info):
        if id is None:
            return FailedReq('Missing item Id')

        title = item_info.get('title')
        year = item_info.get('year')
        genre = item_info.get('genre')
        author = item_info.get('author')
        cover = item_info.get('cover')

        if title is None or title == '':
            return FailedReq('Missing title')

        if year is None or year == '':
            item_info['year'] = 'N/A'

        if author is None or author == '':
            item_info['author'] = 'N/A'

        if genre is None or genre == '':
            item_info['genre'] = 'N/A'

        if cover is None or cover == '':
            item_info['cover'] = self.__default_pic

        return super().edit_item(id, item_info)


class MoviesController(BaseController):
    def __init__(self, db_provider):

        super().__init__(db_provider, 'movies')
        self.__default_pic = os.path.join(
            ROOT_DIR, './assets/default_movie.png'
        )

    def add_item(self, title, year, score, duration, cover):
        if title is None or title == '':
            return FailedReq('Missing title')

        if year is None or year == '':
            year = 'N/A'

        if score is None or score == '':
            score = 'N/A'

        if duration is None or duration == '':
            duration = 'N/A'

        if cover is None or cover == '':
            cover = self.__default_pic

        new_movie = Movie(year, title, cover, duration)
        return super().add_item(new_movie)

    def edit_item(self, id, item_info):
        if id is None:
            return FailedReq('Missing item Id')

        title = item_info.get('title')
        year = item_info.get('year')
        score = item_info.get('score')
        duration = item_info.get('duration')
        cover = item_info.get('cover')

        if title is None or title == '':
            return FailedReq('Missing title')

        if duration is None or duration == '':
            item_info['duration'] = 'N/A'

        if score is None or score == '':
            item_info['score'] = 'N/A'

        if year is None or year == '':
            item_info['year'] = 'N/A'

        if cover is None or cover == '':
            item_info['cover'] = self.__default_pic

        return super().edit_item(id, item_info)

    
