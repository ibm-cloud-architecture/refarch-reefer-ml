# Use an official Python runtime as a parent image
FROM python:3.7-stretch
ENV PATH=/root/.local/bin:/project/deps/bin:$PATH
RUN pip install --upgrade pip \
  && pip install --upgrade --user pipenv

# Set the working directory to /project
WORKDIR /project

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr 
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/project/deps

# Copy the current directory contents into the container server workdir
COPY . ./
RUN pipenv lock -r > requirements.txt 
# Install any needed packages specified in requirements.txt
RUN python -m pip install -r requirements.txt -t /project/deps

EXPOSE 8080

CMD ["python manage.py run -h 0.0.0.0"]

