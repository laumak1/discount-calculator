# Use the official Python base image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the Python scripts and input file into the container
COPY discount_calculator.py .
COPY test_calculator.py .
COPY input.txt .

# Install any dependencies required by your Python script
# If you have any dependencies listed in a requirements.txt file, uncomment the line below
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "discount_calculator.py"]