from abc import ABC, abstractmethod
from user_orm import UserORM


class AbstractBase(ABC):
    @abstractmethod
    def get_user_info(self, user_id: str) -> UserORM:
        pass

    @abstractmethod
    def set_user_info(self, user: UserORM) -> None:
        pass

    @abstractmethod
    def create_tables(self) -> None:
        pass


class UserDoesntExistInDB(Exception):
    pass
