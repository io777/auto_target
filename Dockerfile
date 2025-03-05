FROM python:3.9-slim-buster

# Установка зависимостей
RUN apt-get update && apt-get install -y \
	python3-opencv \
	libgl1-mesa-glx \
	libglib2.0-0 \
	libsm6 \
	libxext6 \
	libxrender-dev \
	libx11-dev \
	v4l-utils \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

CMD ["python3", "detect.py", "--yolo", "yolo"]
