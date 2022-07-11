FROM python:3.9-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000
# ENV PATH="${PATH}:/root/.local/bin"
# ENV PYTHONPATH=.
# RUN pip install --upgrade pip
# FROM redis
# CMD [ "redis-server"]