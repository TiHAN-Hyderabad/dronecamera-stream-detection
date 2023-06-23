# Use the official Ubuntu image as the base image
FROM ubuntu

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y python3 python3-pip libgl1-mesa-glx

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the server.py file to the container
COPY server.py .

# Run the server.py script when the container starts
CMD ["python3", "server.py"]
