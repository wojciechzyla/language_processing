FROM python:3.8-slim
WORKDIR /nlp
COPY . /nlp
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader -d /usr/share/nltk_data punkt
RUN chmod +x gunicorn_starter.sh
EXPOSE 5002
CMD ["python","app.py"]