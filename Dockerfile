# Use a lightweight base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first for better caching
COPY . /app

COPY traffic_classifier.h5 /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5050

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
