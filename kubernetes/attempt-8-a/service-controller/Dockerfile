FROM python:3.7-alpine

RUN pip3 install -q requests==2.21.0 kubernetes==9.0.0
WORKDIR /code
COPY controller.py controller.py

CMD ["python3", "/code/controller.py"]
