FROM python:3.7-alpine

RUN pip3 install -q Flask==1.0.2 requests==2.21.0
RUN mkdir /code
ADD ./service.py /code

CMD ["python3", "/code/service.py"]
