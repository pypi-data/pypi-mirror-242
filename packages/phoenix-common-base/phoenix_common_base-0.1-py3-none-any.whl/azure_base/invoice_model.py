import uuid
import logging
import pandas as pd
from datetime import datetime
from typing import List, Optional


logger = logging.getLogger(__name__)


def prepare_sql_query_value(query_value: str, data_type=str):
    return data_type(query_value) if not pd.isna(query_value) else None


def prepare_date_sql_query_value(query_value: str, date_format: str):
    return (
        format_date(query_value, date_format)
        if not pd.isna(query_value)
        else None
    )


def format_date(date_data: str, date_format: str) -> str:
    return datetime.strptime(date_data, date_format).strftime("%Y-%m-%d")


class InvoiceProperties:
    id: str
    InvoiceID: str
    CustomerInvoiceTermsDescription: str
    BillingCurrency: str
    CreditStatus: str
    InvoiceTermsDescription: str
    CustomerBillingCurrency: str
    CustomerCreditLimit: float
    SalesOrderNumber: str
    SalesOrderDate: str
    PurchaseOrderNumber: str
    StartIssue: str
    LastIssue: str
    CreditCardToken: str
    AmountPaid: float
    TaxAmount: float
    PostageAmount: float
    PostageVAT: float
    TotalAmount: float
    PaymentType: str
    PaymentReference: str
    TaxExemptFlag: str
    InvoiceDueDate: str
    MessageCode: str
    CampaignCode: str
    PrintonDemand: str
    OrderSource: str
    TransactionType: str

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_abs(cls, invoice_id: str, row: dict):
        properties = cls()
        properties.id = str(uuid.uuid4())
        properties.InvoiceID = invoice_id
        properties.CustomerInvoiceTermsDescription = prepare_sql_query_value(row["CustomerInvoiceTermsDescription".upper()])
        properties.BillingCurrency = prepare_sql_query_value(row["BillingCurrency".upper()])
        properties.CreditStatus = prepare_sql_query_value(row["CreditStatus".upper()])
        properties.InvoiceTermsDescription = prepare_sql_query_value(row["InvoiceTermsDescription".upper()])
        properties.CustomerBillingCurrency = prepare_sql_query_value(row["CustomerBillingCurrency".upper()])
        properties.CustomerCreditLimit = prepare_sql_query_value(row["CustomerCreditLimit".upper()], float)
        properties.SalesOrderNumber = prepare_sql_query_value(row["SalesOrderNumber".upper()])
        properties.SalesOrderDate = prepare_date_sql_query_value(row["SalesOrderDate".upper()], "%d-%b-%Y")
        properties.PurchaseOrderNumber = prepare_sql_query_value(row["PurchaseOrderNumber".upper()])
        properties.StartIssue = prepare_sql_query_value(row["StartIssue".upper()])
        properties.LastIssue = prepare_sql_query_value(row["LastIssue".upper()])
        properties.CreditCardToken = prepare_sql_query_value(row["CreditCardToken".upper()])
        properties.AmountPaid = prepare_sql_query_value(row["AmountPaid".upper()], float)
        properties.TaxAmount = prepare_sql_query_value(row["TaxAmount".upper()], float)
        properties.PostageAmount = prepare_sql_query_value(row["PostageAmount".upper()], float)
        properties.PostageVAT = prepare_sql_query_value(row["PostageVAT".upper()], float)
        properties.TotalAmount = prepare_sql_query_value(row["TotalAmount".upper()], float)
        properties.PaymentType = prepare_sql_query_value(row["paymenttype".upper()])
        properties.PaymentReference = prepare_sql_query_value(row["PaymentReference".upper()])
        properties.TaxExemptFlag = prepare_sql_query_value(row["TaxExemptFlag".upper()])
        properties.InvoiceDueDate = prepare_date_sql_query_value(row["InvoiceDueDate".upper()], "%d-%b-%Y")
        properties.MessageCode = prepare_sql_query_value(row["MessageCode".upper()])
        properties.CampaignCode = prepare_sql_query_value(row["CampaignCode".upper()])
        properties.PrintonDemand = prepare_sql_query_value(row["PrintonDemand".upper()])
        properties.OrderSource = prepare_sql_query_value(row["OrderSource".upper()])
        properties.TransactionType = prepare_sql_query_value(row["TransactionType".upper()])

        return properties

    def calculate_total_net(self):
        return self.TotalAmount-(self.PostageAmount+self.TaxAmount+self.PostageVAT)


class InvoiceItem:
    ItemNumber: str
    ItemDescription: str
    Id: str
    InvoiceId: str
    UnitPrice: float
    DiscAmount: float
    NetPrice: float
    TaxCommodityCode: str
    QuantityOrdered: int
    TaxPercent: float
    PackageType: str
    LastIssueDate: str
    YearofPublication: int
    OrderType: str
    SusbcriptionType: str
    RecordType: str

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_abs(cls, invoice_id: str, row: dict):
        item = cls()
        item.Id = str(uuid.uuid4())
        item.InvoiceId = invoice_id
        item.ItemNumber = prepare_sql_query_value(row["ItemNumber".upper()])
        item.ItemDescription = prepare_sql_query_value(row["ItemDescription".upper()])
        item.UnitPrice = prepare_sql_query_value(row["UnitPrice".upper()], float)
        item.DiscAmount = prepare_sql_query_value(row["DiscAmount".upper()], float)
        item.NetPrice = prepare_sql_query_value(row["NetPrice".upper()], float)
        item.TaxCommodityCode = prepare_sql_query_value(row["TaxCommodityCode".upper()])
        item.QuantityOrdered = prepare_sql_query_value(row["QuantityOrdered".upper()], int)
        item.TaxPercent = prepare_sql_query_value(row["TaxPercent".upper()])
        item.PackageType = prepare_sql_query_value(row["PackageType".upper()])
        item.LastIssueDate = prepare_date_sql_query_value(row["LastIssueDate".upper()], "%d/%m/%Y")
        item.YearofPublication = prepare_sql_query_value(row["YearofPublication".upper()], int)
        item.OrderType = prepare_sql_query_value(row["OrderType".upper()])
        item.SusbcriptionType = prepare_sql_query_value(row["SusbcriptionType".upper()])
        item.RecordType = prepare_sql_query_value(row["RecordType".upper()])

        return item


class Address:
    class Address:
        Id: str
        InvoiceId: str
        Type: str
        CustomerNumber: str
        AddressCode: str
        AddressLine1: str
        AddressLine2: str
        AddressLine3: str
        City: str
        State: str
        PostalCode: str
        CountryName: str
        CompanyName: str
        FirstName: str
        MiddleInitial: str
        LastName: str
        EmailAddress: str
        CustomerType: Optional[str]

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_abs(cls, invoice_id: str, row: dict, address_type: str):
        address = cls()
        address.Id = str(uuid.uuid4())
        address.InvoiceId = invoice_id
        address.Type = address_type
        address.CustomerNumber = prepare_sql_query_value(row[f"{address_type}CustomerNumber".upper()])
        address.AddressCode = prepare_sql_query_value(row[f"{address_type}AddressCode".upper()])
        address.AddressLine1 = prepare_sql_query_value(row[f"{address_type}AddressLine1".upper()])
        address.AddressLine2 = prepare_sql_query_value(row[f"{address_type}AddressLine2".upper()])
        address.AddressLine3 = prepare_sql_query_value(row[f"{address_type}AddressLine3".upper()])
        address.City = prepare_sql_query_value(row[f"{address_type}City".upper()])
        address.State = prepare_sql_query_value(row[f"{address_type}State".upper()])
        address.PostalCode = prepare_sql_query_value(row[f"{address_type}PostalCode".upper()])
        address.CountryName = prepare_sql_query_value(row[f"{address_type}CountryCode".upper()])
        address.CompanyName = prepare_sql_query_value(row[f"{address_type}CompanyName".upper()])
        address.FirstName = prepare_sql_query_value(row[f"{address_type}FirstName".upper()])
        address.MiddleInitial = prepare_sql_query_value(row[f"{address_type}MiddleInitial".upper()])
        address.LastName = prepare_sql_query_value(row[f"{address_type}LastName".upper()])
        address.EmailAddress = prepare_sql_query_value(row[f"{address_type}EmailAddress".upper()])
        address.CustomerType = prepare_sql_query_value(row[f"{address_type}CustomerType".upper()]) if row.get(f"{address_type}CustomerType") else None

        return address


class InvoiceFactory:
    def __init__(self, invoice_id: str, invoice_number: str, source: str):
        self.id: str = invoice_id
        self.invoice_number: str = invoice_number
        self.source: str = source
        self.properties: Optional[InvoiceProperties] = None
        self.items: List[InvoiceItem] = []
        self.addresses: List[Address] = []

    def to_dict(self):
        return {
            'Id': self.id,
            'InvoiceNumber': self.invoice_number,
            'Source': self.source
        }

    @classmethod
    def from_abs(cls, invoice_id: str, invoice_number: str, source: str, invoice_data):
        invoice = cls(invoice_id=invoice_id, invoice_number=invoice_number, source=source)
        invoice.properties = InvoiceProperties.from_abs(invoice_id, invoice_data.iloc[0])
        invoice.addresses.append(Address.from_abs(invoice_id, invoice_data.iloc[0], 'BILLTO'))
        invoice.addresses.append(Address.from_abs(invoice_id, invoice_data.iloc[0], 'SHIPFROM'))
        invoice.addresses.append(Address.from_abs(invoice_id, invoice_data.iloc[0], 'SHIPTHROUGH'))
        invoice.addresses.append(Address.from_abs(invoice_id, invoice_data.iloc[0], 'SHIPTO'))
        for line in invoice_data.iloc:
            invoice.items.append(InvoiceItem.from_abs(invoice_id, line))
        return invoice
