# Use Python 3.6.9 as the base image
FROM python:3.6.9

# Copy the directory to /app
WORKDIR /app
COPY . /app

# Create virtual environment for the app and install dependencies
RUN python -m venv venv && \
    /bin/bash -c "source venv/bin/activate && \
    /app/venv/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt"

# Expose port 5000
EXPOSE 5000

# Run server.py
CMD ["venv/bin/python", "server.py"]