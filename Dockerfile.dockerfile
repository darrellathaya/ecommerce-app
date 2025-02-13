# Python image, the base image for building Docker container, this establish environment for the container.
FROM python:3.0-slim

# Sets working directory inside the container, where all the subsequent commands will be executed in this directory. Sets the context for subsequent commands.
WORKDIR /app

#Copies requirements.txt to list all the dependencies needed for python application from the local directory to the current working directory "/app" inside the container. Copied early to leverage Docker layer caching.
COPY requirements.txt .

#Install dependencies listed in requirements.txt, this command placed before the rest of the application files to avoid reinstallation of dependencies if there's a change on the app code.
RUN pip install --upgrade pip && pip install -r requirements.txt

#Copy the rest of the application files from the current directory to the /app directory inside the computer, this includes Python scripts, templates, static files, and other resource needed by application
COPY . .

#Expose the flask port, informs Docker that the container / app will listen on port 5000
EXPOSE 5000

# Specifies the command to run when the container starts
CMD ["python3", "main.py"]