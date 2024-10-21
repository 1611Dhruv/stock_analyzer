FROM python:3.11-slim-buster
FROM sqlite:3.36.0

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

ENV ALPHA_VANTAGE_API_KEY=GX4181VXEDB5XM3A
# Run the startup script which will initialize the project
RUN . ./startup
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

WORKDIR  /app
# Define the command to run your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
