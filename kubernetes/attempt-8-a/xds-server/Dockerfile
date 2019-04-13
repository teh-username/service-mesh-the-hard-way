FROM python:3.7-alpine

RUN pip3 install -q requests==2.21.0 Flask==1.0.2
WORKDIR /code
COPY source/ source/

CMD ["python3", "/code/source/server.py"]
