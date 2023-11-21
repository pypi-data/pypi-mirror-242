import pytest
import logging

from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, ContainerClient, ContainerSasPermissions

from infi_azure import AzureStorageAccount, AzureContainer, AzureBlob
from tests import TestConfig


def instance_azure_container(container_name: str) -> AzureContainer:
    storage_account: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_CONNECTION_STRING)
    return AzureContainer(container_name, storage_account)


def test_init_valid():
    storage_account: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_CONNECTION_STRING)
    container_name: str = TestConfig.TEST_CONTAINER_NAME
    container_client: ContainerClient = storage_account.blob_service_client.get_container_client(container_name)
    assert isinstance(storage_account.blob_service_client, BlobServiceClient)
    assert isinstance(container_name, str)
    assert isinstance(container_client, ContainerClient)


def test_get_all_directories_in_container():
    azure_container: AzureContainer = instance_azure_container(TestConfig.TEST_CONTAINER_NAME)
    assert isinstance(azure_container.get_all_directories_in_container(), list)


def test_generate_sas_token():
    permission: ContainerSasPermissions = ContainerSasPermissions(read=True, write=True, delete=True, list=True,
                                                                  add=True, create=True)
    expiry: datetime = datetime.utcnow() + timedelta(days=365)
    azure_container: AzureContainer = instance_azure_container(TestConfig.TEST_CONTAINER_NAME)
    sas_token: str = azure_container.generate_sas_token(permission, expiry)
    assert isinstance(sas_token, str)


def test_generate_sas_token_not_valid_permission(caplog):
    caplog.set_level(logging.ERROR)
    permission = "not_valid_permission"
    expiry: datetime = datetime.utcnow() + timedelta(days=365)
    azure_container: AzureContainer = instance_azure_container(TestConfig.TEST_CONTAINER_NAME)
    azure_container.generate_sas_token(permission, expiry)
    assert 'Invalid permission' in caplog.text


def test_is_container_exist():
    azure_container: AzureContainer = instance_azure_container(TestConfig.TEST_CONTAINER_NAME)
    assert azure_container.is_container_exist() is True


def test_is_container_not_exist():
    azure_container: AzureContainer = instance_azure_container(TestConfig.TEST_NOT_EXIST_CONTAINER)
    assert azure_container.is_container_exist() is False


def test_delete_blobs_in_directory():
    azure_container: AzureContainer = instance_azure_container(TestConfig.TEST_CONTAINER_NAME)
    blob_name: str = TestConfig.TEST_DELETE_BLOB
    azure_container.container_client.upload_blob(name=blob_name, data=b"test data")
    azure_container.delete_blobs_in_directory(blob_name)
    blob: AzureBlob = AzureBlob(blob_name, azure_container)
    assert blob.is_blob_exist() is False


if __name__ == "__main__":
    pytest.main()
