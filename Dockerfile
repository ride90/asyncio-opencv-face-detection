# Use a Miniconda base image
FROM continuumio/miniconda3

# Install Mamba from the Conda-Forge channel
RUN conda install mamba -n base -c conda-forge

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file, to cache the dependencies installation
COPY requirements.txt /app/

# Use Mamba to install the packages from requirements.txt
RUN mamba install --yes --file requirements.txt || pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Make port 8088 available to the world outside this container
EXPOSE 8088

# Run main.py when the container launches
CMD ["python", "./main.py"]