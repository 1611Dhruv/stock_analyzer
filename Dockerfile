FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install the python requirements
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Check for database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
