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

    def tryexceptwrap(func):
        try:
            return func
        except Exception as e:
            return FailedReq(repr(e))

    def __init__(self, db_provider: DbProvider, target_collection: str):
        self.db_provider = db_provider
        self.target_collection = target_collection

    @abstractmethod
    @tryexceptwrap
    def get_collection(self) -> ControllerMethodOutput:
        collection = self.db_provider.get_db_json()[self.target_collection]
        return FulfilledReq(collection)

    @abstractmethod
    def add_item(self, item) -> ControllerMethodOutput:
        try:
            db_json = self.db_provider.get_db_json()
            db_json[self.target_collection].apppend(item)
            self.db_provider.rewrite_db(db_json)

            return FulfilledReq()
        except Exception as e:
            return FailedReq(repr(e))

    @abstractmethod
    def delete_item(self, id) -> ControllerMethodOutput:
        pass

    @abstractmethod
    def edit_item(self, id, new_entry) -> ControllerMethodOutput:
        pass


class GamesController(BaseController):
    def __init__(self, db_provider):
        super().__init__(db_provider, 'games')

    def add_item(self, item):
        return super().add_item(item)

    def edit_item(self, id: str):
        return super().add_item(id)

    def delete_item(self, id: str):
        return super().delete_item(id)

    def get_collection(self):
        return super().get_collection()
