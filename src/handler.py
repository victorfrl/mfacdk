import typing

from model import AbstractORM


class RequestHandler:
    def __init__(self, orm: AbstractORM) -> None:
        self.orm = orm

    def save(self, item: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return self.orm.create(item)

    def get(self, task_id: str) -> typing.Dict[str, typing.Any]:
        return self.orm.get_by_id(task_id)

    def get_all(self) -> typing.List[typing.Dict[str, typing.Any]]:
        return self.orm.get_all()
