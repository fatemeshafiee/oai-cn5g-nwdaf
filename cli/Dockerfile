FROM python:3.6.9-slim AS nwdaf-cli

COPY ./requirements.txt /tmp
RUN pip install --upgrade pip wheel && \
    pip install -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

WORKDIR /nwdaf-cli
CMD ["sleep", "infinity"]
