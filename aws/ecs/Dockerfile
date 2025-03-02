##Creates the docker image for the FastAPI backend service
# Start from an official Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /src

# Copy the requirements.txt to install dependencies first (for better caching)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application files
COPY . .

# Expose port 8000 for the app to listen on
EXPOSE 8000

# Accept build arguments (these come from .env)
ARG DB_TABLE_NAME

# Set environment variables at build time, making them available at runtime
ENV DB_TABLE_NAME=${DB_TABLE_NAME}

# Set the command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]