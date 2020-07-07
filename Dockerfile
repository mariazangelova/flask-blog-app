FROM python:3.6.5-alpine
COPY requirements.txt /
RUN pip install -r ./requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["app.py"]