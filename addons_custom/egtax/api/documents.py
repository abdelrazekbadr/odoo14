# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = doc_data_from_dict(json.loads(json_string))

from utils import *
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, TypeVar, Callable, Type, cast
import dateutil.parser

@dataclass
class Delivery:
    approach: str
    packaging: str
    date_validity: datetime
    export_port: str
    gross_weight: float
    net_weight: float
    terms: str

    @staticmethod
    def from_dict(obj: Any) -> 'Delivery':
        assert isinstance(obj, dict)
        approach = from_str(obj.get("approach"))
        packaging = from_str(obj.get("packaging"))
        date_validity = from_datetime(obj.get("dateValidity"))
        export_port = from_str(obj.get("exportPort"))
        gross_weight = from_float(obj.get("grossWeight"))
        net_weight = from_float(obj.get("netWeight"))
        terms = from_str(obj.get("terms"))
        return Delivery(approach, packaging, date_validity, export_port, gross_weight, net_weight, terms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approach"] = from_str(self.approach)
        result["packaging"] = from_str(self.packaging)
        result["dateValidity"] = self.date_validity.isoformat()
        result["exportPort"] = from_str(self.export_port)
        result["grossWeight"] = to_float(self.gross_weight)
        result["netWeight"] = to_float(self.net_weight)
        result["terms"] = from_str(self.terms)
        return result


@dataclass
class Discount:
    rate: int
    amount: int

    @staticmethod
    def from_dict(obj: Any) -> 'Discount':
        assert isinstance(obj, dict)
        rate = from_int(obj.get("rate"))
        amount = from_int(obj.get("amount"))
        return Discount(rate, amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rate"] = from_int(self.rate)
        result["amount"] = from_int(self.amount)
        return result


@dataclass
class TaxableItem:
    tax_type: str
    amount: int
    sub_type: str
    rate: int

    @staticmethod
    def from_dict(obj: Any) -> 'TaxableItem':
        assert isinstance(obj, dict)
        tax_type = from_str(obj.get("taxType"))
        amount = from_int(obj.get("amount"))
        sub_type = from_str(obj.get("subType"))
        rate = from_int(obj.get("rate"))
        return TaxableItem(tax_type, amount, sub_type, rate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["taxType"] = from_str(self.tax_type)
        result["amount"] = from_int(self.amount)
        result["subType"] = from_str(self.sub_type)
        result["rate"] = from_int(self.rate)
        return result


@dataclass
class UnitValue:
    currency_sold: str
    amount_egp: int

    @staticmethod
    def from_dict(obj: Any) -> 'UnitValue':
        assert isinstance(obj, dict)
        currency_sold = from_str(obj.get("currencySold"))
        amount_egp = from_int(obj.get("amountEGP"))
        return UnitValue(currency_sold, amount_egp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currencySold"] = from_str(self.currency_sold)
        result["amountEGP"] = from_int(self.amount_egp)
        return result


@dataclass
class InvoiceLine:
    description: str
    item_type: str
    item_code: str
    unit_type: str
    quantity: int
    internal_code: str
    sales_total: int
    total: int
    value_difference: int
    total_taxable_fees: int
    net_total: int
    items_discount: int
    unit_value: UnitValue
    discount: Discount
    taxable_items: List[TaxableItem]

    @staticmethod
    def from_dict(obj: Any) -> 'InvoiceLine':
        assert isinstance(obj, dict)
        description = from_str(obj.get("description"))
        item_type = from_str(obj.get("itemType"))
        item_code = from_str(obj.get("itemCode"))
        unit_type = from_str(obj.get("unitType"))
        quantity = from_int(obj.get("quantity"))
        internal_code = from_str(obj.get("internalCode"))
        sales_total = from_int(obj.get("salesTotal"))
        total = from_int(obj.get("total"))
        value_difference = from_int(obj.get("valueDifference"))
        total_taxable_fees = from_int(obj.get("totalTaxableFees"))
        net_total = from_int(obj.get("netTotal"))
        items_discount = from_int(obj.get("itemsDiscount"))
        unit_value = UnitValue.from_dict(obj.get("unitValue"))
        discount = Discount.from_dict(obj.get("discount"))
        taxable_items = from_list(TaxableItem.from_dict, obj.get("taxableItems"))
        return InvoiceLine(description, item_type, item_code, unit_type, quantity, internal_code, sales_total, total, value_difference, total_taxable_fees, net_total, items_discount, unit_value, discount, taxable_items)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_str(self.description)
        result["itemType"] = from_str(self.item_type)
        result["itemCode"] = from_str(self.item_code)
        result["unitType"] = from_str(self.unit_type)
        result["quantity"] = from_int(self.quantity)
        result["internalCode"] = from_str(self.internal_code)
        result["salesTotal"] = from_int(self.sales_total)
        result["total"] = from_int(self.total)
        result["valueDifference"] = from_int(self.value_difference)
        result["totalTaxableFees"] = from_int(self.total_taxable_fees)
        result["netTotal"] = from_int(self.net_total)
        result["itemsDiscount"] = from_int(self.items_discount)
        result["unitValue"] = to_class(UnitValue, self.unit_value)
        result["discount"] = to_class(Discount, self.discount)
        result["taxableItems"] = from_list(lambda x: to_class(TaxableItem, x), self.taxable_items)
        return result


@dataclass
class Address:
    branch_id: Optional[int] = None
    country: str
    governate: str
    region_city: str
    street: str
    building_number: str
    postal_code: int
    floor: int
    room: int
    landmark: str
    additional_information: str

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        branch_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("branchID"))
        country = from_str(obj.get("country"))
        governate = from_str(obj.get("governate"))
        region_city = from_str(obj.get("regionCity"))
        street = from_str(obj.get("street"))
        building_number = from_str(obj.get("buildingNumber"))
        postal_code = int(from_str(obj.get("postalCode")))
        floor = int(from_str(obj.get("floor")))
        room = int(from_str(obj.get("room")))
        landmark = from_str(obj.get("landmark"))
        additional_information = from_str(obj.get("additionalInformation"))
        return Address(branch_id, country, governate, region_city, street, building_number, postal_code, floor, room, landmark, additional_information)

    def to_dict(self) -> dict:
        result: dict = {}
        result["branchID"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.branch_id)
        result["country"] = from_str(self.country)
        result["governate"] = from_str(self.governate)
        result["regionCity"] = from_str(self.region_city)
        result["street"] = from_str(self.street)
        result["buildingNumber"] = from_str(self.building_number)
        result["postalCode"] = from_str(str(self.postal_code))
        result["floor"] = from_str(str(self.floor))
        result["room"] = from_str(str(self.room))
        result["landmark"] = from_str(self.landmark)
        result["additionalInformation"] = from_str(self.additional_information)
        return result


@dataclass
class Issuer:
    address: Address
    type: str
    id: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Issuer':
        assert isinstance(obj, dict)
        address = Address.from_dict(obj.get("address"))
        type = from_str(obj.get("type"))
        id = int(from_str(obj.get("id")))
        name = from_str(obj.get("name"))
        return Issuer(address, type, id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["address"] = to_class(Address, self.address)
        result["type"] = from_str(self.type)
        result["id"] = from_str(str(self.id))
        result["name"] = from_str(self.name)
        return result


@dataclass
class Payment:
    bank_name: str
    bank_address: str
    bank_account_no: str
    bank_account_iban: str
    swift_code: str
    terms: str

    @staticmethod
    def from_dict(obj: Any) -> 'Payment':
        assert isinstance(obj, dict)
        bank_name = from_str(obj.get("bankName"))
        bank_address = from_str(obj.get("bankAddress"))
        bank_account_no = from_str(obj.get("bankAccountNo"))
        bank_account_iban = from_str(obj.get("bankAccountIBAN"))
        swift_code = from_str(obj.get("swiftCode"))
        terms = from_str(obj.get("terms"))
        return Payment(bank_name, bank_address, bank_account_no, bank_account_iban, swift_code, terms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["bankName"] = from_str(self.bank_name)
        result["bankAddress"] = from_str(self.bank_address)
        result["bankAccountNo"] = from_str(self.bank_account_no)
        result["bankAccountIBAN"] = from_str(self.bank_account_iban)
        result["swiftCode"] = from_str(self.swift_code)
        result["terms"] = from_str(self.terms)
        return result


@dataclass
class Signature:
    signature_type: str
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'Signature':
        assert isinstance(obj, dict)
        signature_type = from_str(obj.get("signatureType"))
        value = from_str(obj.get("value"))
        return Signature(signature_type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["signatureType"] = from_str(self.signature_type)
        result["value"] = from_str(self.value)
        return result


@dataclass
class TaxTotal:
    tax_type: str
    amount: int

    @staticmethod
    def from_dict(obj: Any) -> 'TaxTotal':
        assert isinstance(obj, dict)
        tax_type = from_str(obj.get("taxType"))
        amount = from_int(obj.get("amount"))
        return TaxTotal(tax_type, amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["taxType"] = from_str(self.tax_type)
        result["amount"] = from_int(self.amount)
        return result


@dataclass
class Document:
    issuer: Issuer
    receiver: Issuer
    document_type: str
    document_type_version: str
    date_time_issued: datetime
    taxpayer_activity_code: int
    internal_id: str
    purchase_order_reference: str
    purchase_order_description: str
    sales_order_reference: int
    sales_order_description: str
    proforma_invoice_number: str
    payment: Payment
    delivery: Delivery
    invoice_lines: List[InvoiceLine]
    total_discount_amount: int
    total_sales_amount: int
    net_amount: int
    tax_totals: List[TaxTotal]
    total_amount: int
    extra_discount_amount: int
    total_items_discount_amount: int
    signatures: List[Signature]

    @staticmethod
    def from_dict(obj: Any) -> 'Document':
        assert isinstance(obj, dict)
        issuer = Issuer.from_dict(obj.get("issuer"))
        receiver = Issuer.from_dict(obj.get("receiver"))
        document_type = from_str(obj.get("documentType"))
        document_type_version = from_str(obj.get("documentTypeVersion"))
        date_time_issued = from_datetime(obj.get("dateTimeIssued"))
        taxpayer_activity_code = int(from_str(obj.get("taxpayerActivityCode")))
        internal_id = from_str(obj.get("internalID"))
        purchase_order_reference = from_str(obj.get("purchaseOrderReference"))
        purchase_order_description = from_str(obj.get("purchaseOrderDescription"))
        sales_order_reference = int(from_str(obj.get("salesOrderReference")))
        sales_order_description = from_str(obj.get("salesOrderDescription"))
        proforma_invoice_number = from_str(obj.get("proformaInvoiceNumber"))
        payment = Payment.from_dict(obj.get("payment"))
        delivery = Delivery.from_dict(obj.get("delivery"))
        invoice_lines = from_list(InvoiceLine.from_dict, obj.get("invoiceLines"))
        total_discount_amount = from_int(obj.get("totalDiscountAmount"))
        total_sales_amount = from_int(obj.get("totalSalesAmount"))
        net_amount = from_int(obj.get("netAmount"))
        tax_totals = from_list(TaxTotal.from_dict, obj.get("taxTotals"))
        total_amount = from_int(obj.get("totalAmount"))
        extra_discount_amount = from_int(obj.get("extraDiscountAmount"))
        total_items_discount_amount = from_int(obj.get("totalItemsDiscountAmount"))
        signatures = from_list(Signature.from_dict, obj.get("signatures"))
        return Document(issuer, receiver, document_type, document_type_version, date_time_issued, taxpayer_activity_code, internal_id, purchase_order_reference, purchase_order_description, sales_order_reference, sales_order_description, proforma_invoice_number, payment, delivery, invoice_lines, total_discount_amount, total_sales_amount, net_amount, tax_totals, total_amount, extra_discount_amount, total_items_discount_amount, signatures)

    def to_dict(self) -> dict:
        result: dict = {}
        result["issuer"] = to_class(Issuer, self.issuer)
        result["receiver"] = to_class(Issuer, self.receiver)
        result["documentType"] = from_str(self.document_type)
        result["documentTypeVersion"] = from_str(self.document_type_version)
        result["dateTimeIssued"] = self.date_time_issued.isoformat()
        result["taxpayerActivityCode"] = from_str(str(self.taxpayer_activity_code))
        result["internalID"] = from_str(self.internal_id)
        result["purchaseOrderReference"] = from_str(self.purchase_order_reference)
        result["purchaseOrderDescription"] = from_str(self.purchase_order_description)
        result["salesOrderReference"] = from_str(str(self.sales_order_reference))
        result["salesOrderDescription"] = from_str(self.sales_order_description)
        result["proformaInvoiceNumber"] = from_str(self.proforma_invoice_number)
        result["payment"] = to_class(Payment, self.payment)
        result["delivery"] = to_class(Delivery, self.delivery)
        result["invoiceLines"] = from_list(lambda x: to_class(InvoiceLine, x), self.invoice_lines)
        result["totalDiscountAmount"] = from_int(self.total_discount_amount)
        result["totalSalesAmount"] = from_int(self.total_sales_amount)
        result["netAmount"] = from_int(self.net_amount)
        result["taxTotals"] = from_list(lambda x: to_class(TaxTotal, x), self.tax_totals)
        result["totalAmount"] = from_int(self.total_amount)
        result["extraDiscountAmount"] = from_int(self.extra_discount_amount)
        result["totalItemsDiscountAmount"] = from_int(self.total_items_discount_amount)
        result["signatures"] = from_list(lambda x: to_class(Signature, x), self.signatures)
        return result


@dataclass
class DocData:
    documents: List[Document]

    @staticmethod
    def from_dict(obj: Any) -> 'DocData':
        assert isinstance(obj, dict)
        documents = from_list(Document.from_dict, obj.get("documents"))
        return DocData(documents)

    def to_dict(self) -> dict:
        result: dict = {}
        result["documents"] = from_list(lambda x: to_class(Document, x), self.documents)
        return result


def doc_data_from_dict(s: Any) -> DocData:
    return DocData.from_dict(s)


def doc_data_to_dict(x: DocData) -> Any:
    return to_class(DocData, x)
