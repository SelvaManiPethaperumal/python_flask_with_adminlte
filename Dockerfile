FROM python:3.8-slim

# Set environment variables to avoid warnings
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Install pip and virtualenv
RUN pip install --upgrade pip virtualenv

RUN mkdir /usr/app
RUN mkdir /usr/app/Logs
COPY . /usr/app
WORKDIR /usr/app

# Create and activate a virtual environment
RUN virtualenv venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get update && apt-get install vim telnet -y && apt autoremove -y
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install -r requirements.txt
RUN export PATH=$PATH:/path/to/pg_config


# Copy the entire application directory into the container
COPY . .

# Make the directory where files will be uploaded
RUN mkdir -p usr/app/app/data


EXPOSE 80
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["python", "app.py", "runserver","--dir=/usr/app"]
