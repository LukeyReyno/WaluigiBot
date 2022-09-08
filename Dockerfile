FROM python:3

COPY . /waluigibot

WORKDIR /waluigibot

RUN python3 -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -qq && apt-get -y install \
      vim

RUN echo "export PATH=/waluigibot/data/CExecutables:${PATH}" >> /root/.bashrc

RUN mkdir exec

CMD python3 -u WaluigiBot.py > log.txt 2>&1