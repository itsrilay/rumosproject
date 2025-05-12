# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create and set the working directory
WORKDIR /rumosproject

# Copy the requirements file into the container
COPY requirements.txt .

# Install pip and any needed dependencies in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create .env file
RUN echo "$ENV_FILE" > .env

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 80, default HTTP port
EXPOSE 80

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:80"]