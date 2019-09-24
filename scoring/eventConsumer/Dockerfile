# Use an official Python runtime as a parent image
FROM python:3.7-stretch
# Set the working directory to /app


# Copy the current directory contents into the container at /app
COPY . /listener
WORKDIR listener
# Install any needed packages specified in requirements.txt
RUN  pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variable
ENV KAFKA_BROKERS kafka1:9092
ENV KAFKA_ENV LOCAL
ENV KAFKA_API ""

CMD ["python", "ScoringAgent.py"]


