FROM python:3.6.3-slim

ADD bridge/ /bridge/
WORKDIR /bridge/

RUN pip install --upgrade -r requirements.txt

CMD [ "python", "pearl.py" ]
