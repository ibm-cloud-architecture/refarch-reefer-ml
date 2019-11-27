# Use an official Python runtime as a parent image
FROM python:3.7-stretch
RUN pip install --upgrade pip \
  && pip install --upgrade --user pipenv
ENV PATH=/root/.local/bin:/project/deps/bin:$PATH

# Set the working directory to /project
WORKDIR /project

# Copy the current directory contents into the container server workdir
COPY . ./
RUN pipenv lock -r > requirements.txt
# Install any needed packages specified in requirements.txt
RUN python -m pip install -r requirements.txt -t /project/deps

ENV PYTHONPATH=/project/deps

# Define environment variable
ENV KAFKA_BROKERS kafka1:9092
ENV KAFKA_API ""
ENV KAFKA_CERT ""

EXPOSE 8080
# Runs container API when started
CMD ["gunicorn", "-b", "0.0.0.0:8080" , "app"]

# CMD ["python app.py"]

