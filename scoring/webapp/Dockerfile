# Use an official Python runtime as a parent image
FROM python:3.7-stretch
# Set the working directory to /app
WORKDIR server

# Copy the current directory contents into the container at /app
COPY . /server

# Install any needed packages specified in requirements.txt
RUN  pip install --trusted-host pypi.python.org -r requirements.txt

ENV PREDICT_WEB_PORT 8083
EXPOSE ${PREDICT_WEB_PORT}

CMD ["gunicorn", "-b", "0.0.0.0:" + ${PREDICT_WEB_PORT}, "wsgi"]


