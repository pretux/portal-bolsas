FROM python:3.9

ENV FLASK_APP run.py
ENV CLEARDB_DATABASE_URL=mysql://bbf35257344c98:1c73d01e@us-cdbr-east-03.cleardb.com/heroku_d2c2b2995bca6b1?reconnect=true
COPY run.py requirements* config.py .env ./
COPY app app

RUN pip install -r requirements-pgsql.txt

RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 80
CMD    ["flask", "run","--host=0.0.0.0", "--port=80"]
