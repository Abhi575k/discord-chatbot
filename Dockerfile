FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y

COPY ./requirements/ ./

RUN apt install python3 python3-pip -y

COPY ./ /root/

RUN pip3 install -r /root/requirements/pip

CMD python3 /root/bot/bot/bot.py