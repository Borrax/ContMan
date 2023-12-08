from abc import abstractmethod, ABC
from typing import Union

from db_provider import DbProvider

type ControllerMethodOutput = Union[FulfilledReq, FailedReq]


class FulfilledReq:
    def __init__(self, payload=None):
        self.payload = payload


class FailedReq:
    def __init__(self, err_msg=None):
        self.err_msg = err_msg


class BaseController(ABC):
    db_provider = None
    target_collection = None

    @abstractmethod
    def __init__(self, db_provider: DbProvider, target_collection: str):
        self.db_provider = db_provider
        self.target_collection = target_collection

    def tryexceptwrap(func):
        try:
            return func
        except Exception as e:
            return FailedReq(repr(e))

    @tryexceptwrap
    def get_collection(self) -> ControllerMethodOutput:
        collection = self.db_provider.get_db_json()[self.target_collection]
        return FulfilledReq(collection)

    @tryexceptwrap
    def add_item(self, item) -> ControllerMethodOutput:
        db_json = self.db_provider.get_db_json()
        db_json[self.target_collection].add(item)
        self.db_provider.rewrite_db(db_json)

    @tryexceptwrap
    def delete_item(self, id) -> ControllerMethodOutput:
        pass

    @tryexceptwrap
    def edit_item(self, id, new_entry) -> ControllerMethodOutput:
        pass


class GamesController(BaseController):
    def __init__(self, db_provider):
        super().__init__(db_provider, 'games')
