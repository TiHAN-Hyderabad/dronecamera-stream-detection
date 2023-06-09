# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY server.py .
COPY templates/index.html .

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]
