FROM docker/compose:alpine-1.25.3

RUN apk update && apk add python3 python3-dev py-pip

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /
WORKDIR /

CMD ["python3", "-u", "shiprat.py"]
