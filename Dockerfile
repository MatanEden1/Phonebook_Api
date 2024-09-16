FROM python:3.12.5

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "run_app", "run", "--host=0.0.0.0"]
