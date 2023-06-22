FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y

COPY ./requirements/ ./

RUN apt install python3 python3-pip cron -y

COPY ./ /root/

RUN pip3 install -r /root/requirements/pip

RUN chmod +x /root/run_dagster

RUN service cron start

RUN echo "0 * * * * /root/run_dagster" >> scheduler
RUN crontab scheduler

RUN service cron start

CMD python3 /root/bot/bot/bot.py