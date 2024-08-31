# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory to /app
WORKDIR /app

# Update and install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    curl \
    apt-transport-https \
    wget

# Clean up to reduce layer size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

EXPOSE 80

# Run the startup script
CMD streamlit run app.py --server.port 80 --server.enableXsrfProtection false