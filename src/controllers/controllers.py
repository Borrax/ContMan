import os
from abc import abstractmethod, ABC
from typing import Union

from config import ROOT_DIR
from db_provider import DbProvider
from models.models import Movie
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

    @abstractmethod
    def __init__(self, db_provider: DbProvider, target_collection: str):
        self.__db_provider = db_provider
        self.__target_collection = target_collection
        self.default_movie_pic = os.path.join(
            ROOT_DIR, './assets/default_movie.png'
        )

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
        return FulfilledReq()

    @__tryexceptwrap
    def edit_item(self, new_item) -> ControllerMethodOutput:
        id = new_item.id
        db_json = self.db_provider.get_db_json()
        if db_json[self.__target_collection].get(id) is None:
            return FailedReq('Not existing id of the item')

        db_json[self.__target_collection][id] = new_item
        return FulfilledReq()


class GamesController(BaseController):
    def __init__(self, db_provider):
        super().__init__(db_provider, 'games')


class BooksController(BaseController):
    def __init__(self, db_provider):
        super().__init__(db_provider, 'books')


class MoviesController(BaseController):
    def __init__(self, db_provider):
        super().__init__(db_provider, 'movies')

    def add_item(self, title, year, score, duration):
        if title is None or title == '':
            return FailedReq('Missing title')

        if year is None or year == '':
            year = 'N/A'

        if score is None or score == '':
            score = 'N/A'

        if duration is None or duration == '':
            duration = 'N/A'

        cover = self.default_movie_pic
        new_movie = Movie(year, title, cover, duration)
        return super().add_item(new_movie)
