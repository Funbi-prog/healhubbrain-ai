FROM rasa/rasa:3.6.20-full

COPY . /app
WORKDIR /app

RUN rasa train

EXPOSE 5005
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
