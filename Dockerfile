FROM python:3

WORKDIR /app

COPY ./app/requirements.txt ./
COPY ./miniusos.sql ./

RUN pip install -r requirements.txt

COPY ./app ./

EXPOSE 5000

CMD ["flask", "--app", "strona", "run", "--host=0.0.0.0", "--port=5000"]
