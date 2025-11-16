FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    py3-pip

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

ENTRYPOINT ["sh", "-c"]
CMD ["alembic upgrade head && uvicorn main:app --host 0.0.0.0 --proxy-headers --port 8000 --root-path=\"/api\" "]
