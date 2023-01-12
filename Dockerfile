FROM python:3.11.1-alpine
LABEL maintainer="klusowskimat@gmail.com"

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk update && apk add libpq-dev python3-dev &&\
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp 

ENV PATH="/py/bin:$PATH"

CMD ["python", "main.py"]