# Datasets Server Python SDK

This is the Python SDK for using the [Huggingface Datasets Server](https://github.com/huggingface/datasets-server). It is not the official SDK, but it is a good start. 
I will try to keep it up to date with the latest version of the Datasets Server.

## Installation

```bash
pip install datasets-server-service
```

## Usage

```python
from datasets_server_service import DatasetsServerService

# You can give your api token here or pass it as HF_DATASETS_SERVER_TOKEN env variable
service = DatasetsServerService()
valid_datasets = service.valid_datasets()
```