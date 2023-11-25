import typing
import uuid
from abc import ABC, abstractmethod

from pydantic import BaseModel


class TaskDTO(BaseModel):
    task_id: str = str(uuid.uuid4())
    name: str
    description: str
    completed: bool = False


class AbstractORM(ABC):
    @abstractmethod
    def get_by_id(self, task_id: str) -> typing.Dict[str, typing.Any]:
        ...

    @abstractmethod
    def create(
        self, item: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        ...

    @abstractmethod
    def update(self, task_id: str, item: dict) -> typing.Dict[str, typing.Any]:
        ...

    @abstractmethod
    def delete(self, task_id: str) -> typing.Dict[str, typing.Any]:
        ...

    @abstractmethod
    def get_all(self) -> typing.List[typing.Dict[str, typing.Any]]:
        ...
