# 🎥 YouTube Downloader API (FastAPI + Docker Compose)

A FastAPI-based service to download YouTube videos using **yt-dlp**, fully containerized with Docker Compose.

---

## 🐳 Run with Docker Compose

### 1. Build and start containers
```bash
docker-compose up -d --build
```

### 2. Stop containers
```bash
docker-compose up down
```
## 3. Linting with Ruff

Run Ruff to check code style and linting:

```bash
ruff check .
```

## 🔗 API Endpoints

- **`GET /download/?url=<video_url>`** → start a new download  
- **`GET /status/{job_id}`** → check download status  
- **`GET /files/{filename}`** → fetch completed file  

Visit the interactive docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

