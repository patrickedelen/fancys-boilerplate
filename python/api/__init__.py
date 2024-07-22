import logging

from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult

from worker.app import app as celery_app
from worker.app import add

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/hello")
async def read_hello():
    """
    get endpoint that returns a hello world message
    """
    return {"message": "Hello, World!"}


@app.post("/add/{x}/{y}")
def add_numbers(x: int, y: int, background_tasks: BackgroundTasks):
    """
    add two numbers together using celery background tasks
    """

    task = add.apply_async(args=[x, y])
    background_tasks.add_task(task.wait)

    return {"task_id": task.id, "status": task.status}


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    """
    get the result for the task based on id using sqlalchemy database backend
    """
    logger.info(f"checking backend for result: {celery_app._get_backend()}")

    result = AsyncResult(task_id, app=celery_app)

    if result.state == 'SUCCESS':
        return {"task_id": task_id, "status": result.state, "result": result.info}

    return {"task_id": task_id, "status": result.state}
