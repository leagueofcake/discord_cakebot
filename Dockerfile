FROM python:3.8.2

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bot .

CMD ["python", "./run.py"]
