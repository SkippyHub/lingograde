# Build frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend

# Install dependencies and build
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Build backend
FROM python:3.11-slim
WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend build to nginx's serve directory
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html/

# Install backend dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application code
COPY . .

# Cloud Run will set PORT environment variable
ENV PORT=8000

# Start both nginx and uvicorn
CMD ["sh", "-c", "service nginx start && poetry run uvicorn app.api.main:app --host 0.0.0.0 --port $PORT"]