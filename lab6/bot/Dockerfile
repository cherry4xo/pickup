FROM python:3.11.6-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env

RUN apt-get -y update
RUN python3.11 -m pip install --no-cache-dir -r /code/requirements.txt
RUN apt-get install -y inkscape

COPY ./app /code/app
RUN mkdir -p /usr/share/fonts/truetype/
# COPY ./data/fonts/ /code/fonts/
RUN install -m644 /code/app/data/fonts/*.ttf /usr/share/fonts/truetype/
COPY ./main.py /code/main.py

CMD ["python3.11", "-u", "main.py"]
