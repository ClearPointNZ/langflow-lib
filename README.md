# langflow-lib

## How to Use

Components can be pulled into your Langflow instance by setting the `LANGFLOW_BUNDLE_URLS` environment variable to the URL of this repository.

For example:
```
docker run --rm -it -p 7860:7860 -e LANGFLOW_BUNDLE_URLS="https://github.com/ClearPointNZ/langflow-lib" langflowai/langflow
```
Note: The command above will not perist any workflows or configuration. Use for testing only