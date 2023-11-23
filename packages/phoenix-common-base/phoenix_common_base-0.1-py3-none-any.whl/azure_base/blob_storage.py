from azure.storage.blob import BlobServiceClient


class BlobStorageConnector:
    def __init__(self, connection_string: str):
        self.client = BlobServiceClient.from_connection_string(connection_string)

    def get_container_client(self, container_name: str):
        return self.client.get_container_client(container_name)

    def get_blob_client(self, container_name: str, blob_name: str):
        source_container_client = self.get_container_client(container_name)
        return source_container_client.get_blob_client(blob_name)

    def close_connection(self):
        self.client.close()
