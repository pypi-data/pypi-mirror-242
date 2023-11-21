import pytest
import os
import logging

from infi_azure import AzureStorageAccount, AzureContainer, azcopy_action, AzureBlob
from tests import TestConfig


def instance_azure_container(container_name: str):
    storage_account: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_CONNECTION_STRING)
    return AzureContainer(container_name, storage_account)


def test_azcopy_action():
    from_container: AzureContainer = instance_azure_container(TestConfig.TEST_FROM_CONTAINER_NAME)
    to_container: AzureContainer = instance_azure_container(TestConfig.TEST_TO_CONTAINER_NAME)

    source_url: str = from_container.generate_url(TestConfig.TEST_FROM_DIRECTORY)
    destination_url: str = to_container.generate_url(TestConfig.TEST_TO_DIRECTORY)

    azcopy_action(os.environ["azcopy"], source_url, destination_url)
    copied_blob: AzureBlob = AzureBlob(TestConfig.TEST_TO_DIRECTORY, to_container)

    assert copied_blob.is_blob_exist() is True
    to_container.delete_blobs_in_directory(TestConfig.TEST_TO_DIRECTORY)


def test_azcopy_action_error(caplog):
    caplog.set_level(logging.ERROR)

    from_container: AzureContainer = instance_azure_container(TestConfig.TEST_FROM_CONTAINER_NAME)
    to_container: AzureContainer = instance_azure_container(TestConfig.TEST_TO_CONTAINER_NAME)

    source_url: str = from_container.generate_url(TestConfig.TEST_FROM_DIRECTORY)
    destination_url: str = to_container.generate_url(TestConfig.TEST_TO_DIRECTORY)

    azcopy_action("azcopy_invalid_path", source_url, destination_url)
    assert 'FileNotFoundError' in caplog.text


if __name__ == "__main__":
    pytest.main()
