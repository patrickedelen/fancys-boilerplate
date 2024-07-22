from utils.envs import envs
from utils.database import get_sync_db_url
from celery import Celery
print('Hello worker!')


# envs = Envs()
app = Celery('tasks', broker=envs.RABBITMQ_BROKER, backend=get_sync_db_url())

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@app.task
def add(x: int, y: int) -> int:
    return x + y


print('testtests')
