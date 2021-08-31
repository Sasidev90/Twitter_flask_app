FROM library/python:3.6

RUN apt-get update && apt-get install nano

ADD . /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY templates ./usr/src/app

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD python app.py
