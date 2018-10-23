FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-dev
COPY ./requirements.txt /tmp/requirements.txt
WORKDIR ./tmp
RUN pip3 install -r requirements.txt
WORKDIR /backend
CMD ["python3", "backend_app.py"]
