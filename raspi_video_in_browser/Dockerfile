# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y  libgl1-mesa-glx

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server.py file to the container
COPY server.py .

# Expose the desired port (9001 in this case)
EXPOSE 9001

# Run the server.py script when the container starts
CMD ["python", "server.py"]

