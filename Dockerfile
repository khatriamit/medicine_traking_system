FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/app
CMD ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
