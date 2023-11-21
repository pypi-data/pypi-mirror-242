import pytest

from azure.storage.blob import ContainerClient, BlobClient

from infi_azure import AzureStorageAccount, AzureContainer, AzureBlob
from tests import TestConfig


def instance_azure_blob(blob_name: str) -> AzureBlob:
    storage_account: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_CONNECTION_STRING)
    azure_container: AzureContainer = AzureContainer(TestConfig.TEST_CONTAINER_NAME, storage_account)
    return AzureBlob(blob_name, azure_container)


def test_init_valid():
    storage_account: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_CONNECTION_STRING)
    azure_container: AzureContainer = AzureContainer(TestConfig.TEST_CONTAINER_NAME, storage_account)
    blob_name: str = TestConfig.TEST_BLOB_NAME
    blob_client: BlobClient = azure_container.container_client.get_blob_client(blob_name)
    assert isinstance(azure_container.container_client, ContainerClient)
    assert isinstance(blob_name, str)
    assert isinstance(blob_client, BlobClient)


def test_download_blob():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_BLOB_NAME)
    assert isinstance(azure_blob.download_blob(), bytes)


def test_is_blob_exist():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_BLOB_NAME)
    assert azure_blob.is_blob_exist() is True


def test_is_blob_not_exist():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_NOT_EXIST_BLOB)
    assert azure_blob.is_blob_exist() is False


def test_is_not_empty_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_NOT_EMPTY_BLOB_NAME)
    assert azure_blob.is_empty_directory() is False


def test_is_empty_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_EMPTY_BLOB_NAME)
    assert azure_blob.is_empty_directory() is True


def test_create_empty_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_CREATE_EMPTY_BLOB)
    azure_blob.create_empty_directory()
    assert azure_blob.is_empty_directory() is True
    azure_blob.azure_container.delete_blobs_in_directory(TestConfig.TEST_CREATE_EMPTY_BLOB)


def test_count_blobs_in_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_BLOB_NAME)
    assert isinstance(azure_blob.count_blobs_in_directory(), int)


if __name__ == "__main__":
    pytest.main()
