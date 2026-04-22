# Use a lightweight Python 3.10 base image
FROM python:3.10-slim

# Set the working directory inside the container to /app
# WORKDIR /app  # Uvicorn will try to run /app/main.py
# but main.py is in Backend_Knowledge_Assistant/
WORKDIR /app/Backend_Knowledge_Assistant    

# Copy backend requirements FIRST (best for Docker caching)
COPY Backend_Knowledge_Assistant/requirements.txt ./requirements.txt

# Install Python dependencies (no cache to keep image small)
RUN pip install --no-cache-dir -r requirements.txt

# # Copy all backend code (API + AI agents + configs) into the container
# COPY . .

# COPY BOTH backend + AI folder explicitly
COPY Backend_Knowledge_Assistant /app/Backend_Knowledge_Assistant
COPY AI_Knowledge_Assistant /app/AI_Knowledge_Assistant

# Set PYTHONPATH so the RAG module (AI_Knowledge_Assistant) becomes importable as a package within the container
ENV PYTHONPATH=/app

# Inform Docker that the container will listen on port 8000
EXPOSE 8000

# Start the FastAPI app using Uvicorn when the container runs
# main:app → app object inside main.py
# 0.0.0.0 → allow external access (required for Docker)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]