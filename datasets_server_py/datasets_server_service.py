import os
from typing import List, Optional

import requests
from pydantic import BaseModel, Field


class DatasetRow(BaseModel):
    row_idx: int = Field(..., description="The index of the row")
    row: dict = Field(
        ..., description="The content of the row, with one field for each column"
    )
    truncated_cells: Optional[List[str]] = Field(
        [], description="The list of truncated cells. See Truncated responses."
    )


class Feature(BaseModel):
    feature_idx: int = Field(..., description="The index of the column")
    name: str = Field(..., description="The name of the column")
    type: dict = Field(
        ..., description="the feature type as defined by the 🤗 Datasets library"
    )


class DatasetSplit(BaseModel):
    dataset: str = Field(..., description="The name of the dataset")
    config: str = Field(..., description="The name of the configuration")
    split: str = Field(..., description="The name of the split")
    num_bytes: Optional[int] = Field(
        None, description="The size of the split in bytes. Can be None"
    )
    num_examples: Optional[int] = Field(
        None, description="The number of examples in the split. Can be None"
    )


class DatasetFirstRows(BaseModel):
    dataset: str = Field(..., description="The name of the dataset")
    config: str = Field(..., description="The name of the configuration")
    split: str = Field(..., description="The name of the split")
    features: List[Feature] = Field(..., description="The list of features")
    rows: List[DatasetRow] = Field(..., description="The list of rows")


class DatasetsServerService:
    BASE_API_URL = "https://datasets-server.huggingface.co"

    def __init__(self, api_token: str = None):
        """Initialize the DatasetsServerService

        Args:
            api_token: The API token to use to access the datasets server.
                       If None, the token will be read from the HF_DATASETS_SERVER_TOKEN environment variable.
                       Some functions will not work if no token is provided.
        """
        if not api_token:
            self.api_token = os.environ.get("HF_DATASETS_SERVER_TOKEN", "")
            return

        self.api_token = api_token

    def _check_response(self, response: requests.Response):

        if response.status_code == 401:
            raise Exception("Invalid API token")

        if response.status_code == 404:
            error = response.json()["error"]
            raise Exception(error)

        if response.status_code == 500:
            error = response.json()["error"]
            cause = response.json()["cause_message"]
            raise Exception(f"Error: {error}. Cause: {cause}")

    def valid_datasets(self) -> List[str]:
        """Get the list of valid datasets

        Some Hub repositories cannot be loaded with the 🤗 Datasets library, for example because the data has still
        to be uploaded, or the format is not supported. The API endpoints will return an error for such datasets.


        Currently, only the streamable datasets are supported, to allow extracting the 100 first rows
        without downloading the whole dataset.

        Returns:
            A list of valid datasets
        """
        response = requests.get(f"{self.BASE_API_URL}/valid")

        self._check_response(response)

        return response.json().get("valid", [])

    def is_valid_dataset(self, dataset_name: str) -> bool:
        """Checks whether a specific dataset loads without any error.

        Args:
            dataset_name: The name of the dataset

        Returns:
            A list of DatasetSplit objects
        """

        headers = (
            {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
        )

        response = requests.get(
            f"{self.BASE_API_URL}/is-valid",
            params={"dataset": dataset_name},
            headers=headers,
        )

        self._check_response(response)

        result = response.json()["valid"]

        return result

    def splits(self, dataset_name: str) -> List[DatasetSplit]:
        """Get the list of configurations and splits of a dataset.

         The datasets aimed at training and evaluating a Machine Learning model are generally divided into
         multiple splits, for example train, test and validation. Some datasets also use configurations (sub-datasets)
         to group similar examples: CommonVoice’s configurations embed the audio recordings of each language ;
         GLUE provides one configuration for every evaluation task.


        Args:
            dataset_name: The name of the dataset

        Returns:
            A list of DatasetSplit objects
        """

        headers = (
            {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
        )

        response = requests.get(
            f"{self.BASE_API_URL}/splits",
            params={"dataset": dataset_name},
            headers=headers,
        )

        self._check_response(response)

        result = [DatasetSplit(**item) for item in response.json()["splits"]]

        return result

    def first_rows(
        self, dataset_name: str, config: str, split: str
    ) -> DatasetFirstRows:
        """Get the columns and the first rows of a dataset split.

        The response is a JSON. The first 100 rows, or all the rows if the split contains less than 100 rows,
        are returned under the rows key. The list of columns (called features to stick with the datasets library)
        contain the data type and are returned under the features key.
        The dataset, config and split fields are also provided in the response.

        When the response size for 100 rows is too big, the last rows are removed until the response size is under 1MB.

        If even the first rows generate a response that does not fit within the limit, the content of the cells
        themselves is truncated and converted to a string.

        In this case, the truncated cells are listed in the truncated_cells field.

        Args:
            dataset_name: The name of the dataset
            config: The name of the configuration
            split: The name of the split

        Returns:
            A DatasetFirstRows object
        """

        headers = (
            {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
        )

        response = requests.get(
            f"{self.BASE_API_URL}/first-rows",
            params={"dataset": dataset_name, "config": config, "split": split},
            headers=headers,
        )

        self._check_response(response)

        result = DatasetFirstRows(**response.json())

        return result
