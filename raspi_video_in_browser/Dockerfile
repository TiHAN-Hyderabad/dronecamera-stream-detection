FROM python:3.9

WORKDIR /app

RUN apt update && apt install python3-pip -y && apt install ffmpeg -y

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY yolov5su.pt .

COPY server.py .

CMD ["python3", "server.py"]
