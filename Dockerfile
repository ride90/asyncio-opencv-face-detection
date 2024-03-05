# This Dockerfile is designed to work on arm64.

# Start with a Python 3.8 slim image that supports arm64
FROM python:3.8-slim


# Ensure system is updated and has basic build requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel
RUN apt-get update && apt-get install -y build-essential libffi-dev

# Pre-install numpy to avoid build issues, preferring binary wheels
RUN pip install --prefer-binary numpy==1.19.2

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first, to leverage Docker cache
COPY requirements.txt /app/

# Install any additional requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8088

# Command to run the application
CMD ["python", "./main.py"]
