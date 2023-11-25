import boto3

from . import AbstractORM


class DynamoORM(AbstractORM):
    def get_all(self) -> list:
        return self.table.scan()["Items"]

    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def get_by_id(self, task_id: str) -> dict:
        item = self.table.get_item(Key={"task_id": task_id})
        return item.get("Item")

    def create(self, item: dict) -> dict:
        self.table.put_item(Item=item)
        return item

    def update(self, task_id: str, item: dict) -> dict:
        return self.table.update_item(
            Key={"task_id": task_id}, AttributeUpdates=item, ReturnValues="UPDATED_NEW"
        )

    def delete(self, task_id: str) -> dict:
        return self.table.delete_item(Key={"task_id": task_id})
