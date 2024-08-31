FROM --platform=linux/amd64 python:3.10
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libpq-dev

ENV PYTHONBUFFERED 1
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]