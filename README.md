# langflow-lib

## How to Use

# via Bundle URLs
Components can be pulled into your Langflow instance by setting the `LANGFLOW_BUNDLE_URLS` environment variable to the URL of this repository.

For example:
```
docker run --rm -it -p 7860:7860 -e LANGFLOW_BUNDLE_URLS="https://github.com/ClearPointNZ/langflow-lib" langflowai/langflow
```
Note: The command above will not persist any workflows or configuration. Use for testing only

Many of these components require additional Python packages to be installed. These will need to be available in your Langflow instance. See the `comps_requirements.txt` file for a list of dependencies.

# Via custom docker image
Alternatively you can build a custom docker container with the depencies and the components installed. For example:

``` dockerfile
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
```