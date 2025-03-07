# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose fastapi[all]

# Expose the port the service runs on
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "auth_main:app", "--host", "0.0.0.0", "--port", "8001"]
