# Use an official Python runtime as a parent image
FROM python:3.7-stretch
# Set the working directory to /app
WORKDIR server

# Copy the current directory contents into the container at /app
COPY . /server

# Install any needed packages specified in requirements.txt
RUN  pip install --trusted-host pypi.python.org -r requirements.txt


# Define environment variable
ENV KAFKA_BROKERS kafka1:9092
ENV KAFKA_API ""
ENV KAFKA_CERT /opt/app-root/src/es-cert.pem
EXPOSE 8080
# Runs container API when started
CMD ["gunicorn", "-b", "0.0.0.0:8080" , "wsgi"]


