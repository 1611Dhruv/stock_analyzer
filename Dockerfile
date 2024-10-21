FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

ENV ALPHA_VANTAGE_API_KEY=GX4181VXEDB5XM3A
# Run the startup script which will initialize the project
RUN . ./startup

WORKDIR  /app/stock_analyzer
# Define the command to run your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
