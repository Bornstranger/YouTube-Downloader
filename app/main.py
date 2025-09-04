import os
import uuid

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.worker import DOWNLOAD_DIR, download_video_task

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download/")
async def download_video(url: str = Query(...)) -> dict:
    """Endpoint to initiate video download."""
    job_id = str(uuid.uuid4())
    download_video_task.delay(url, job_id)
    return {"job_id": job_id, "status": "processing"}

@app.get("/status/{job_id}")
async def check_status(job_id: str) -> dict:
    """Endpoint to check the status of a download job."""
    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    if os.path.exists(filepath):
        return {"status": "completed", "download_url": f"{filepath}"}
    return {"status": "processing"}

@app.get("/files/{filename}")
async def get_file(filename: str) -> FileResponse:
    """Endpoint to fetch the downloaded video file."""
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not ready yet")
    return FileResponse(filepath, filename=filename, media_type="video/mp4")
