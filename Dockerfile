FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y git ffmpeg libffi-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "bot.py"]
