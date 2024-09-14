# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /build

# Install dependencies in a separate layer
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy installed python packages from builder
COPY --from=builder /install /usr/local

# Copy project files (excluding those matched by .dockerignore)
COPY . .

# Collect static files
RUN python FlowerLensBackend/manage.py collectstatic --noinput

# Expose the port Django runs on by default (8000)
EXPOSE 8000

# Specify the command to run your application
CMD ["python", "FlowerLensBackend/manage.py", "runserver", "0.0.0.0:8000"]
