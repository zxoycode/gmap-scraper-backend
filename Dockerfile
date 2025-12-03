FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 安裝 Playwright + Chromium
RUN playwright install --with-deps chromium

COPY . .

# Railway 會設定 $PORT 環境變數，這裡用它，如果沒有就用 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
