from typing import NamedTuple, List


class UserORM(NamedTuple):
    id: str
    tasks: List
    projects: List
