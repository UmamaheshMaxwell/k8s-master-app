# You can use any python base image you prefer
FROM python:3.9-slim

# Create a working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY templates/ ./templates/

# Expose port 80 for our FastAPI app
EXPOSE 80

# Run the uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
