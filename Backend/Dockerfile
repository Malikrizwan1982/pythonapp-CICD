# Use a slim Python image for a smaller footprint
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]