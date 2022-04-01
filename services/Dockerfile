FROM python:3.9.10-bullseye

WORKDIR /.

COPY . .

RUN pip install flask --upgrade pip
RUN pip install redis
RUN pip install aioflask

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["main.py"]