import os
from pathlib import Path

import yt_dlp
from celery import Celery

DOWNLOAD_DIR = Path(__file__).parent.parent / "downloads"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

celery = Celery(
    "worker",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
)

@celery.task
def download_video_task(url: str, job_id: str) -> str:
    """Celery task to download video using yt-dlp."""
    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    ydl_opts = {"outtmpl": filepath, "format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filepath
