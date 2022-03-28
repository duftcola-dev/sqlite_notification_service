FROM python:3.9.10-bullseye

RUN mkdir -p /home/app

COPY . /home/app

RUN pip install flask --upgrade pip

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["/home/app/main.py"]