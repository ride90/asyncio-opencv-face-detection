ARG PYTHON_VERSION="3.8.6"
FROM python:${PYTHON_VERSION}-slim-buster

LABEL mantainer="Chao Yang Wu <peteeelol@gmail.com>"

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install numpy

ARG OPENCV_VERSION="4.4.0.44"
ARG SYSTEM_CORES="8"
RUN cp /usr/bin/make /usr/bin/make.bak && \
    echo "make.bak --jobs=${SYSTEM_CORES} \$@" > /usr/bin/make && \
    pip install -v opencv-python==${OPENCV_VERSION} && \
    mv /usr/bin/make.bak /usr/bin/make \

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
