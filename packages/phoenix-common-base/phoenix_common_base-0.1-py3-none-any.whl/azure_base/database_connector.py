from pyodbc import connect, Error
import uuid
import json
import logging
from datetime import datetime

from .invoice_model import InvoiceFactory
from enum import Enum
from .validator import InvoiceValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DataMartTables(Enum):
    Invoice = "Invoice"
    InvoiceProperties = "InvoiceProperties"
    InvoiceItem = "InvoiceItem"
    Address = "Address"
    FileHistory = "FileHistory"
    ErrorReport = "ErrorReport"


class DatabaseConnector:
    def __init__(self, server, database, username, password, driver='{ODBC Driver 17 for SQL Server}'):
        self.conn = connect(
            f"Driver={driver};"
            f"Server={server}.database.windows.net;"
            f"Database={database};"
            f"UID={username};"
            f"PWD={password}"
        )
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str, *params):
        try:
            self.cursor.execute(query, *params)
            return self.cursor.fetchall()
        except Error as e:
            logging.error(f"Error executing query: {e}")
            return None

    def execute_non_query(self, query: str, *params) -> bool:
        try:
            self.cursor.execute(query, *params)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(f"Error executing non-query: {e}")
            return False

    def begin_transaction(self):
        self.conn.autocommit = False

    def commit_transaction(self):
        self.conn.commit()

    def rollback_transaction(self):
        self.conn.rollback()


class InvoicesManager:
    def __init__(self, server: str, database: str, username: str, password: str):
        self.db_manager = DatabaseConnector(server, database, username, password)
        self.validator = InvoiceValidator()

    def insert_invoices(self, source: str, file_name: str, dataframe) -> bool:
        logger.info(self._prepare_log(message=f"Processing file: {file_name}"))
        self.db_manager.begin_transaction()
        for invoice_number, invoice_data in dataframe:
            invoice_id = str(uuid.uuid4())
            invoice = InvoiceFactory.from_abs(invoice_id, invoice_number, source, invoice_data)
            logger.info(self._prepare_log(f"Processing invoice. Invoice number: {invoice_number}"))
            self.insert_query(invoice.to_dict(), DataMartTables.Invoice.value)
            self.insert_query(invoice.properties.to_dict(), DataMartTables.InvoiceProperties.value)
            for address in invoice.addresses:
                self.insert_query(address.to_dict(), DataMartTables.Address.value)
            for item in invoice.items:
                self.insert_query(item.to_dict(), DataMartTables.InvoiceItem.value)
            self.validator.validate_invoice(invoice)
            self.insert_invoice_history(invoice_id=invoice_id, file_name=file_name, source=source)
        self.insert_errors()
        self.db_manager.commit_transaction()
        self.db_manager.disconnect()
        return True

    def update_invoices(self, source: str, file_name: str, dataframe):
        logger.info(self._prepare_log(message=f"Processing file: {file_name}"))
        self.db_manager.begin_transaction()
        for invoice_number, invoice_data in dataframe:
            invoice_id = self.get_invoice_id(invoice_number, source)
            logger.info(self._prepare_log(f"Processing invoice. Invoice number: {invoice_number}"))
            if invoice_id:
                self.delete_invoice_related_records(invoice_id)
                invoice = InvoiceFactory.from_abs(invoice_id, invoice_number, source, invoice_data)
            else:
                invoice_id = str(uuid.uuid4())
                invoice = InvoiceFactory.from_abs(invoice_id, invoice_number, source, invoice_data)
                self.insert_query(invoice.to_dict(), DataMartTables.Invoice.value)
            self.insert_query(invoice.properties.to_dict(), DataMartTables.InvoiceProperties.value)
            for address in invoice.addresses:
                self.insert_query(address.to_dict(), DataMartTables.Address.value)
            for item in invoice.items:
                self.insert_query(item.to_dict(), DataMartTables.InvoiceItem.value)
            self.validator.validate_invoice(invoice)
            self.insert_invoice_history(invoice_id=invoice_id, file_name=file_name, source=source)
        self.insert_errors()
        self.db_manager.commit_transaction()
        self.db_manager.disconnect()
        return True

    def get_invoice_id(self, invoice_number: str, source: str):
        query = "SELECT Id FROM Invoice WHERE InvoiceNumber = ? AND Source = ?"
        result = self.db_manager.execute_query(query, invoice_number, source)
        return result[0][0] if result else None

    def delete_invoice_related_records(self, invoice_id: str) -> None:
        self.db_manager.execute_non_query("DELETE FROM InvoiceItem WHERE InvoiceId = ?", invoice_id)
        self.db_manager.execute_non_query("DELETE FROM InvoiceProperties WHERE InvoiceId = ?", invoice_id)
        self.db_manager.execute_non_query("DELETE FROM Address WHERE InvoiceId = ?", invoice_id)
        self.db_manager.execute_non_query("DELETE FROM ErrorReport WHERE InvoiceId = ?", invoice_id)

    def insert_invoice_history(self, invoice_id: str, file_name: str, source: str) -> None:
        import_date = datetime.now()
        query_data = {
            "Id": str(uuid.uuid4()),
            "InvoiceId": invoice_id,
            "FileName": file_name,
            "ProcessedAt": import_date,
            "Source": source
        }
        self.insert_query(query_data, DataMartTables.FileHistory.value)

    def insert_errors(self) -> None:
        for error in self.validator.errors:
            query_data = {
                "Id": str(uuid.uuid4()),
                "InvoiceId": error['invoice_id'],
                "Code": error['error_code'],
                "Description": error['description']
            }
            self.insert_query(query_data, DataMartTables.ErrorReport.value)

    def insert_query(self, query_data: dict, table_name: str) -> None:
        try:
            self.db_manager.execute_non_query(
                self._create_insert_query(query_data, table_name),
                *tuple(query_data.values())
            )
        except Exception as e:
            logger.info(self._prepare_log(f"Error during insert query processing {str(e)}"))

    @staticmethod
    def _prepare_log(message: str) -> json:
        return json.dumps(
            {
                "Source": "ABS",
                "Message": message
            }
        )

    @staticmethod
    def _create_insert_query(data: dict, table: str) -> str:
        placeholders = ", ".join(["?"] * len(data))
        columns_query_string = ", ".join(data.keys())
        return f"INSERT INTO {table} ({columns_query_string}) VALUES ({placeholders})"
