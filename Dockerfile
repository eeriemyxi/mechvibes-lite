FROM python:3.12

RUN pip install uv

WORKDIR /mechvibes-lite
COPY . .

RUN uv sync

CMD uv run mvibes -L DEBUG wskey --host 0.0.0.0 --port 80 daemon
