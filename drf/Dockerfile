###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.13 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get -y install postgresql-server-dev-all gcc libpq-dev python3-dev musl-dev -y

# lint
RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.13-bullseye

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/mediafiles
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install libpq-dev python3-dev -y
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

RUN sed -i 's/staticfiles/static/g' /usr/local/lib/python3.9/site-packages/rest_framework_swagger/templates/rest_framework_swagger/index.html

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
