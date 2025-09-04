import uuid
import os

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.worker import download_video_task, DOWNLOAD_DIR

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
async def download_video(url: str = Query(...)):
    job_id = str(uuid.uuid4())
    download_video_task.delay(url, job_id)
    return {"job_id": job_id, "status": "processing"}

@app.get("/status/{job_id}")
async def check_status(job_id: str):
    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    if os.path.exists(filepath):
        return {"status": "completed", "download_url": f"{filepath}"}
    return {"status": "processing"}

@app.get("/files/{filename}")
async def get_file(filename: str):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not ready yet")
    return FileResponse(filepath, filename=filename, media_type="video/mp4")
