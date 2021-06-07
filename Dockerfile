FROM python:3.9
COPY . /
RUN pip install -r requirements.txt
WORKDIR /
CMD ["echo", "The bot is about to start!"]
ENTRYPOINT ["python3"]
CMD ["./main.py"]
