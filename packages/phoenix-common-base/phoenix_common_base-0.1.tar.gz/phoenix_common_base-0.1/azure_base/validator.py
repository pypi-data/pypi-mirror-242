from enum import Enum
import re
from .helper_methods import isclose, issn_pattern
from .invoice_model import InvoiceFactory
from .validators.invoice_schema_validators import ItemSchemaValidator, AddressSchemaValidator, PropertiesSchemaValidator


class ErrorCode(Enum):
    VALUE_ISSUE_ERROR = "02001"  # Contains required values, types, formats, regex
    DUPLICATED_INVOICE = "02002"
    INBALANCED_INVOICE = "02003"
    CUSTOMER_NOT_FOUND = "02004"
    PRODUCT_NOT_FOUND = "02005"
    UNKNOWN_ISSN = "02006"
    INVALID_ISSN_FORMAT = "02007"
    NEGATIVE_NUMBERS = "02008"
    INVALID_LINE_CALCULATION = "02009"
    INVOICE_NUMBER_EMPTY = "02010"


class InvoiceValidator:

    def __init__(self):
        self.address_schema_validator = AddressSchemaValidator()
        self.properties_schema_validator = PropertiesSchemaValidator()
        self.item_schema_validator = ItemSchemaValidator()
        self.errors = []

    def validate_invoice(self, inv: InvoiceFactory) -> None:
        self.validate_items(inv)
        self.validate_address(inv)
        self.validate_properties(inv)

    def validate_address(self, inv: InvoiceFactory) -> None:
        # Validate required values and types
        for address in inv.addresses:
            for error in self.address_schema_validator.validate_schema(address.to_dict()):
                self.errors.append({
                    "invoice_id": inv.id,
                    "error_code": ErrorCode.VALUE_ISSUE_ERROR.value,
                    "description": f"Address value error: {error} in Invoice: {inv.invoice_number}"
                })

    def validate_items(self, inv: InvoiceFactory) -> None:
        for item in inv.items:
            # Validate required values and types
            for error in self.item_schema_validator.validate_schema(item.to_dict()):
                self.errors.append({
                    "invoice_id": inv.id,
                    "error_code": ErrorCode.VALUE_ISSUE_ERROR.value,
                    "description": f"Item value error: {error} in Invoice: {inv.invoice_number}"
                })
            # Has negative numbers
            if any(isinstance(value, float) and value < 0 for value in vars(item).values()):
                self.errors.append({
                    "invoice_id": inv.id,
                    "error_code": ErrorCode.NEGATIVE_NUMBERS.value,
                    "description": f"Negative numbers in Invoice: {inv.invoice_number}, Item: {item.ItemNumber}"
                })
            # Has invalid ISSN
            if not (issn_pattern.match(item.ItemNumber)) and not re.search(r'-\d{4}$', item.ItemNumber):
                self.errors.append({
                    "invoice_id": inv.id,
                    "error_code": ErrorCode.INVALID_ISSN_FORMAT.value,
                    "description": f"Invalid ISSN in Invoice: {inv.invoice_number}, ISSN: {item.ItemNumber}"
                })

    def validate_properties(self, inv: InvoiceFactory) -> None:
        # Validate required values and types
        for error in self.properties_schema_validator.validate_schema(inv.properties.to_dict()):
            self.errors.append({
                "invoice_id": inv.id,
                "error_code": ErrorCode.VALUE_ISSUE_ERROR.value,
                "description": f"Properties value error: {error} in Invoice: {inv.invoice_number}"
            })
        # Validate invoice balance
        items_net_sum = sum(item.NetPrice for item in inv.items)
        invoice_total_net = inv.properties.calculate_total_net()
        if not isclose(items_net_sum, invoice_total_net):
            self.errors.append({
                "invoice_id": inv.id,
                "error_code": ErrorCode.INBALANCED_INVOICE.value,
                "description": f"Invoice total net: {invoice_total_net} mismatch with Items net sum: {items_net_sum}"
            })
