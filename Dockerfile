FROM langflowai/langflow:latest

#USER root
#RUN chown -R root:root /app
COPY requirements.txt /tmp/requirements.txt

RUN /app/.venv/bin/python -m ensurepip --upgrade && \
    /app/.venv/bin/python -m pip install --upgrade pip && \
    /app/.venv/bin/python -m pip install wheel 

RUN /app/.venv/bin/python -m pip install --no-cache-dir -r /tmp/requirements.txt


CMD ["langflow", "run"]