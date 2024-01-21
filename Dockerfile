# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Port to expose
EXPOSE 5000

# Set the working directory
WORKDIR /app2

# Copy the contents of the current directory into the container at /app
COPY . /app2

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["python", "app2.py", "--server.port=5000", "--server.address=0.0.0.0"]
