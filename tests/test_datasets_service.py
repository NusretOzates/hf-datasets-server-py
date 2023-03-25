import pytest

from datasets_server_py import DatasetsServerService


@pytest.fixture()
def dataset_server_service():
    return DatasetsServerService()


def test_valid_datasets(dataset_server_service):
    datasets = dataset_server_service.valid_datasets()
    assert len(datasets) > 0


def test_is_valid_dataset(dataset_server_service):
    assert dataset_server_service.is_valid_dataset("glue")
    with pytest.raises(Exception):
        dataset_server_service.is_valid_dataset("invalid_dataset")


def test_splits(dataset_server_service):
    splits = dataset_server_service.splits("glue")
    assert len(splits) > 0
    assert splits[0].dataset == "glue"


def test_first_rows(dataset_server_service):
    first_rows = dataset_server_service.first_rows("glue", "sst2", "train")
    assert len(first_rows.rows) > 0
    assert first_rows.dataset == "glue"
    assert first_rows.split == "train"
    assert first_rows.config == "sst2"


def test_parquet(dataset_server_service):
    parquet = dataset_server_service.parquet("glue")
    assert len(parquet) > 0
    assert parquet[0].dataset == "glue"
