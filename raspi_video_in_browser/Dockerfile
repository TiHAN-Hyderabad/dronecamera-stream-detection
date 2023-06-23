# Use the official Ubuntu base image
FROM ubuntu

# Set the working directory in the container
WORKDIR /app

COPY Dockerfile /app/Dockerfile

# Update package lists and install necessary dependencies
RUN apt update && apt install python3-pip -y && apt install ffmpeg -y

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the server code into the container
COPY server.py .

# Expose the server port
EXPOSE 8080

# Run the server
CMD ["python3", "server.py"]
