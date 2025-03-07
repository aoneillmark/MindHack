# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic requests google-genai

# Expose the port FastAPI will run on
EXPOSE 8002

# Command to run the application
CMD ["uvicorn", "scraped_data_microservice:app", "--host", "0.0.0.0", "--port", "8002"]
