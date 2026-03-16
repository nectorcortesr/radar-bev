FROM python:3.10-slim

# OpenCV necesita libGL para renderizar ventanas
# y libglib para el backend de captura de video. Sin ellas: ImportError en runtime.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest"]