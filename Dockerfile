FROM debian:bookworm

# Install dependencies

RUN apt-get update && apt-get install python3 -y && apt-get install python3-dev -y && apt-get install python3-venv -y
RUN apt-get install cron -y 
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY . /app

# Install dependencies:
COPY requirements.txt /app/
RUN pip install -r requirements.txt


EXPOSE 8448
CMD ["flask", "run", "--host=0.0.0.0", "--port=8448"]