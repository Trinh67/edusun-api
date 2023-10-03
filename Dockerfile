FROM python:3.9.16-slim-buster as compile-image

RUN apt-get -y update && apt-get -y --no-install-recommends install git default-libmysqlclient-dev build-essential pkg-config

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


FROM python:3.9.16-slim-buster
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
ADD . /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]