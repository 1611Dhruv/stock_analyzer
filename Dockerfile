FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install the python requirements
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE $PORT

# Run migrations and then start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT"]
