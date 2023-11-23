import os
from abc import ABC
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from . import constants


class KeyVaultConnector(ABC):

    def __init__(self, key_vault_name: str):
        self.client = SecretClient(vault_url=f"https://{key_vault_name}-{os.environ['STAGE']}.vault.azure.net",
                                   credential=DefaultAzureCredential())

    def get_secret_value(self, secret_name: str):
        return self.client.get_secret(secret_name)

    def close_connection(self):
        self.client.close()


class SecretsInterface(KeyVaultConnector):

    def __init__(self):
        super().__init__(key_vault_name=constants.INTEGRATOR_KEY_VAULT_NAME)


class NotificationSecretsInterface(KeyVaultConnector):

    def __init__(self):
        super().__init__(key_vault_name=constants.NOTIFICATION_KEY_VAULT_NAME)
