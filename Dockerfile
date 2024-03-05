# Start with an official Python image compatible with ARM64 architecture
FROM jjanzic/docker-python3-opencv

# Set the working directory in the container
WORKDIR /app

# Upgrade pip and install wheel to avoid potential issues with package installations
RUN pip install --upgrade pip setuptools wheel

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
# Note: Adjustments might be needed if opencv-python still fails to install
RUN pip install -r requirements.txt

# Copy the rest of your application into the container
COPY . /app

# Expose the port your app runs on
EXPOSE 8080

# Command to run your application
CMD ["python", "./main.py"]
