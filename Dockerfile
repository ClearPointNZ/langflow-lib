FROM langflowai/langflow:latest

# add 3rd party libaries
COPY comps_requirements.txt /tmp/requirements.txt

RUN /app/.venv/bin/python -m ensurepip --upgrade && \
    /app/.venv/bin/python -m pip install --upgrade pip && \
    /app/.venv/bin/python -m pip install wheel 

RUN /app/.venv/bin/python -m pip install --no-cache-dir -r /tmp/requirements.txt

# add components
COPY components/ /app/components/
ENV LANGFLOW_COMPONENTS_PATH=/app/components

CMD ["langflow", "run"]