FROM python:3.12.7-slim-bullseye

WORKDIR /opt/app

COPY ./requirements.txt /opt/app/
RUN pip install  -r requirements.txt

COPY . /opt/app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]