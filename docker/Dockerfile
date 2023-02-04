FROM python:3.10.9-bullseye

WORKDIR /code

RUN apt-get update -y && apt-get install -y --no-install-recommends \
  libgeos-dev \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt
ADD ./grenzeit ./grenzeit

CMD ["python3", "-m", "grenzeit.services.asgi"]