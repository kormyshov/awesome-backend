import json
from typing import List

from abstract_base import AbstractBase, UserDoesntExistInDB
from user_orm import UserORM


class User:
    def __init__(self, chat_id: str, database: AbstractBase) -> None:
        self.id: str = chat_id
        self.database: AbstractBase = database
        self.loaded: bool = False
        self.tasks: List = []
        self.projects: List = []

    def __str__(self) -> str:
        return 'User(id: {}, tasks: {}, projects: {})'.format(
            self.id,
            str(self.tasks),
            str(self.projects),
        )

    def load(self) -> None:
        if not self.loaded:
            try:
                response: UserORM = self.database.get_user_info(self.id)
                self.tasks = response.tasks
                self.projects = response.projects
            except UserDoesntExistInDB:
                pass

            self.loaded = True

    def save(self) -> None:
        self.database.set_user_info(UserORM(
            id=self.id,
            tasks=self.tasks,
            projects=self.projects,
        ))

    def get_tasks_str(self) -> str:
        self.load()
        return json.dumps(self.tasks)

    def set_tasks_str(self, tasks: str) -> None:
        self.tasks = json.loads(tasks)

    def get_projects_str(self) -> str:
        self.load()
        return json.dumps(self.projects)

    def set_projects_str(self, projects: str) -> None:
        self.projects = json.loads(projects)
