import yt_dlp
import os
from celery import Celery

DOWNLOAD_DIR = "/app/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

celery = Celery(
    "worker",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://"
)

@celery.task
def download_video_task(url: str, job_id: str):
    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    ydl_opts = {"outtmpl": filepath, "format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filepath
