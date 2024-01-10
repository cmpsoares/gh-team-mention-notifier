FROM python:3.9-slim

# Copy the repository contents into the container at / (root)
COPY . /

# Set the working directory to /
WORKDIR /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests

# Run notify_webhook.py when the container launches
ENTRYPOINT ["python", "./src/notify_webhook.py"]
