# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install build dependencies for psutil and other potential packages
# Clean up apt cache to keep the image size small
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY app/ ./app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# Use uvicorn to run the FastAPI app
# --host 0.0.0.0 makes the server accessible from outside the container
# --port 8000 specifies the port
# --reload is for development, remove in production for better performance
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

