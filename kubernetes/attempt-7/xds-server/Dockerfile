FROM python:3.7-alpine

RUN pip3 install -q Flask==1.0.2
RUN mkdir /code
ADD ./server.py /code

CMD ["python3", "/code/server.py"]
