FROM python:3.12

RUN pip install --no-cache-dir --upgrade pip
RUN pip install pydantic

WORKDIR .
COPY ./graphs.py .
# COPY ./GraphGenerator


CMD ["python", "./graphs.py"]