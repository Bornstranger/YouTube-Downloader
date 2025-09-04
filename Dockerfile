FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set PYTHONPATH so Python can find the 'app' module
ENV PYTHONPATH=/app

# Install runtime dependencies + testing/lint tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app
COPY ./app ./app

# Create downloads directory
RUN mkdir -p /app/downloads

# Expose FastAPI port
EXPOSE 8000

# Default command: run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

