import pyodbc
from enum import Enum


class DataMartTables(Enum):
    Invoice = "Invoice"
    InvoiceProperties = "InvoiceProperties"
    InvoiceItem = "InvoiceItem"
    Address = "Address"


class SqlDatabaseConnector:
    def __init__(
        self,
        datamart_server_name: str,
        datamart_database_name: str,
        datamart_server_login: str,
        datamart_server_password: str,
    ):
        self.connection = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            f"Server={datamart_server_name}.database.windows.net;"
            f"Database={datamart_database_name};"
            f"UID={datamart_server_login};"
            f"PWD={datamart_server_password}"
        )

    def close_connection(self):
        self.connection.close()
