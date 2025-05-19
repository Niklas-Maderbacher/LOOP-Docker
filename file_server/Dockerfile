FROM python:3.12-slim

WORKDIR /file_server

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define environment variable
ENV FLASK_APP=server/server.py
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
