FROM python:3.9-slim

# Copy the repository contents into the container at /app
COPY . /app

# Debug: List contents of /app
RUN ls -la /app

# Set the working directory to /app
WORKDIR /app

# Debug: List contents of /app/src
RUN ls -la /app/src/

# Install any needed dependencies
RUN pip install --no-cache-dir requests

# Run the script
ENTRYPOINT ["python", "/app/src/notify_webhook.py"]
