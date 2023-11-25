import os
import typing
import uuid

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from handler import RequestHandler
from model import TaskDTO
from model.dynamo_orm import DynamoORM

SERVICE_NAME = "task-service"

tracer = Tracer()
logger = Logger(service=SERVICE_NAME)
metrics = Metrics(service=SERVICE_NAME, namespace="TaskService")
metrics.set_default_dimensions(environment="PROD")
app = APIGatewayRestResolver()

TABLE_NAME = os.getenv("TABLE_NAME")

orm = DynamoORM(TABLE_NAME)

request_handler = RequestHandler(orm)


@app.get("/items/<item_id>")
@tracer.capture_method
def get_item_by_id(item_id: str) -> dict:
    logger.info(TABLE_NAME)
    try:
        task = request_handler.get(item_id)
    except Exception as e:
        logger.error(e)
        raise e
    return task if task else {"message": "Task not found"}


@app.get("/items")
@tracer.capture_method
def get_items() -> list:
    metrics.add_metric(name="InvocationsGetItems", unit="Count", value=1)
    logger.info(TABLE_NAME)
    try:
        tasks = request_handler.get_all()
    except Exception as e:
        logger.error(e)
        raise e
    return tasks


@app.post("/items")
@tracer.capture_method
def create_item() -> typing.Any:
    payload: dict = app.current_event.json_body
    metrics.add_metric(name="InvocationsCreateItem", unit="Count", value=1)
    try:
        _task_dto = TaskDTO(
            task_id=str(uuid.uuid4()),
            name=payload["name"],
            description=payload["description"],
            completed=False,
        )
    except ValidationError as ve:
        logger.error(ve)
        return ve.errors()
    except Exception as e:
        logger.error(e)
        raise e
    return request_handler.save(_task_dto.dict())


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
