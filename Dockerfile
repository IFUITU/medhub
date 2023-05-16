FROM python:3.8

ENV WORKDIR=/app

WORKDIR ${WORKDIR}



ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  


RUN pip install --upgrade pip \
    pip install --upgrade setuptools

COPY ./requirements.txt ${WORKDIR}

RUN pip install --default-timeout=100 -r requirements.txt

COPY . ${WORKDIR}

EXPOSE 8000

# CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
ENTRYPOINT ["sh", "/app/entrypoint.sh"]