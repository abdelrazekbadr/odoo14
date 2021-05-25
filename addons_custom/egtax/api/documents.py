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
from ..api.documents import *
from .utils import *
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, TypeVar, Callable, Type, cast
from . import *
import dateutil.parser


# region Submit Document
# https://sdk.invoicing.eta.gov.eg/api/05-submit-documents/
@dataclass
class Delivery:
    approach = ''
    packaging = ''
    date_validity = ''
    export_port = ''
    country_of_origin = ''
    gross_weight = 0.0
    net_weight = 0.0
    terms = ''

    @staticmethod
    def from_dict(obj: Any) -> 'Delivery':
        assert isinstance(obj, dict)
        approach = from_str(obj.get("approach"))
        packaging = from_str(obj.get("packaging"))
        date_validity = from_str(obj.get("dateValidity"))
        export_port = from_str(obj.get("exportPort"))
        country_of_origin = from_str(obj.get("countryOfOrigin"))
        gross_weight = from_float(obj.get("grossWeight"))
        net_weight = from_float(obj.get("netWeight"))
        terms = from_str(obj.get("terms"))
        return Delivery(approach, packaging, date_validity, export_port, country_of_origin, gross_weight, net_weight,
                        terms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approach"] = from_str(self.approach)
        result["packaging"] = from_str(self.packaging)
        result["dateValidity"] = from_str(self.date_validity)
        result["exportPort"] = from_str(self.export_port)
        result["countryOfOrigin"] = from_str(self.country_of_origin)
        result["grossWeight"] = to_float(self.gross_weight)
        result["netWeight"] = to_float(self.net_weight)
        result["terms"] = from_str(self.terms)
        return result


@dataclass
class Discount:
    rate = 0.0
    amount = 0.0

    @staticmethod
    def from_dict(obj: Any) -> 'Discount':
        assert isinstance(obj, dict)
        rate = from_float(obj.get("rate"))
        amount = from_float(obj.get("amount"))
        return Discount(rate, amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rate"] = to_float(self.rate)
        result["amount"] = to_float(self.amount)
        return result


@dataclass
class TaxableItem:
    tax_type = ''
    amount = 0.0
    sub_type = ''
    rate = 0.0

    @staticmethod
    def from_dict(obj: Any) -> 'TaxableItem':
        assert isinstance(obj, dict)
        tax_type = from_str(obj.get("taxType"))
        amount = from_float(obj.get("amount"))
        sub_type = from_str(obj.get("subType"))
        rate = from_float(obj.get("rate"))
        return TaxableItem(tax_type, amount, sub_type, rate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["taxType"] = from_str(self.tax_type)
        result["amount"] = to_float(self.amount)
        result["subType"] = from_str(self.sub_type)
        result["rate"] = to_float(self.rate)
        return result


@dataclass
class UnitValue:
    currency_sold = ''
    amount_egp = 0.0
    amount_sold = 0.0
    currency_exchange_rate = 0.0

    @staticmethod
    def from_dict(obj: Any) -> 'UnitValue':
        assert isinstance(obj, dict)
        currency_sold = from_str(obj.get("currencySold"))
        amount_egp = from_float(obj.get("amountEGP"))
        amount_sold = from_float(obj.get("amountSold"))
        currency_exchange_rate = from_float(obj.get("currencyExchangeRate"))
        return UnitValue(currency_sold, amount_egp, amount_sold, currency_exchange_rate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currencySold"] = from_str(self.currency_sold)
        result["amountEGP"] = to_float(self.amount_egp)
        result["amountSold"] = to_float(self.amount_sold)
        result["currencyExchangeRate"] = to_float(self.currency_exchange_rate)
        return result


@dataclass
class InvoiceLine:
    description = ''
    item_type = ''
    item_code = ''
    unit_type = ''
    quantity = 0.0
    internal_code = ''
    sales_total = 0.0
    total = 0.0
    value_difference = 0.0
    total_taxable_fees = 0.0
    net_total = 0.0
    items_discount = 0.0
    unit_value = UnitValue()
    discount = Discount()
    taxable_items = list()  #: List[TaxableItem]

    @staticmethod
    def from_dict(obj: Any) -> 'InvoiceLine':
        assert isinstance(obj, dict)
        description = from_str(obj.get("description"))
        item_type = from_str(obj.get("itemType"))
        item_code = from_str(obj.get("itemCode"))
        unit_type = from_str(obj.get("unitType"))
        quantity = from_float(obj.get("quantity"))
        internal_code = from_str(obj.get("internalCode"))
        sales_total = from_float(obj.get("salesTotal"))
        total = from_float(obj.get("total"))
        value_difference = from_float(obj.get("valueDifference"))
        total_taxable_fees = from_float(obj.get("totalTaxableFees"))
        net_total = from_float(obj.get("netTotal"))
        items_discount = from_float(obj.get("itemsDiscount"))
        unit_value = UnitValue.from_dict(obj.get("unitValue"))
        discount = Discount.from_dict(obj.get("discount"))
        taxable_items = from_list(TaxableItem.from_dict, obj.get("taxableItems"))
        return InvoiceLine(description, item_type, item_code, unit_type, quantity, internal_code, sales_total, total,
                           value_difference, total_taxable_fees, net_total, items_discount, unit_value, discount,
                           taxable_items)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_str(self.description)
        result["itemType"] = from_str(self.item_type)
        result["itemCode"] = from_str(self.item_code)
        result["unitType"] = from_str(self.unit_type)
        result["quantity"] = to_float(self.quantity)
        result["internalCode"] = from_str(self.internal_code)
        result["salesTotal"] = to_float(self.sales_total)
        result["total"] = to_float(self.total)
        result["valueDifference"] = to_float(self.value_difference)
        result["totalTaxableFees"] = to_float(self.total_taxable_fees)
        result["netTotal"] = to_float(self.net_total)
        result["itemsDiscount"] = to_float(self.items_discount)
        result["unitValue"] = to_class(UnitValue, self.unit_value)
        result["discount"] = to_class(Discount, self.discount)
        result["taxableItems"] = from_list(lambda x: to_class(TaxableItem, x), self.taxable_items)
        return result


@dataclass
class Address:
    country = ''
    governate = ''
    region_city = ''
    street = ''
    building_number = ''
    postal_code = ''
    floor = ''
    room = ''
    landmark = ''
    additional_information = ''
    branch_id = ''

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        country = from_str(obj.get("country"))
        governate = from_str(obj.get("governate"))
        region_city = from_str(obj.get("regionCity"))
        street = from_str(obj.get("street"))
        building_number = from_str(obj.get("buildingNumber"))
        postal_code = from_str(obj.get("postalCode"))
        floor = from_str(obj.get("floor"))
        room = from_str(obj.get("room"))
        landmark = from_str(obj.get("landmark"))
        additional_information = from_str(obj.get("additionalInformation"))
        branch_id = from_union([from_str, from_none], obj.get("branchID"))
        return Address(country, governate, region_city, street, building_number, postal_code, floor, room, landmark,
                       additional_information, branch_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["country"] = from_str(self.country)
        result["governate"] = from_str(self.governate)
        result["regionCity"] = from_str(self.region_city)
        result["street"] = from_str(self.street)
        result["buildingNumber"] = from_str(self.building_number)
        result["postalCode"] = from_str(self.postal_code)
        result["floor"] = from_str(self.floor)
        result["room"] = from_str(self.room)
        result["landmark"] = from_str(self.landmark)
        result["additionalInformation"] = from_str(self.additional_information)
        result["branchID"] = from_union([from_str, from_none], self.branch_id)
        return result


@dataclass
class Partner:
    address = Address()
    type = ''
    id = ''
    name = ''

    @staticmethod
    def from_dict(obj: Any) -> 'Partner':
        assert isinstance(obj, dict)
        address = Address.from_dict(obj.get("address"))
        type = from_str(obj.get("type"))
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return Partner(address, type, id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["address"] = to_class(Address, self.address)
        result["type"] = from_str(self.type)
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class Payment:
    bank_name = ''
    bank_address = ''
    bank_account_no = ''
    bank_account_iban = ''
    swift_code = ''
    terms = ''

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
    signature_type = ''
    value = ''

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
    amount: float

    @staticmethod
    def from_dict(obj: Any) -> 'TaxTotal':
        assert isinstance(obj, dict)
        tax_type = from_str(obj.get("taxType"))
        amount = from_float(obj.get("amount"))
        return TaxTotal(tax_type, amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["taxType"] = from_str(self.tax_type)
        result["amount"] = to_float(self.amount)
        return result


@dataclass
class Document:
    issuer = Partner()
    receiver = Partner()
    document_type = ''
    document_type_version = ''
    date_time_issued = ''
    taxpayer_activity_code = ''
    internal_id = ''
    purchase_order_reference = ''
    purchase_order_description = ''
    sales_order_reference = ''
    sales_order_description = ''
    proforma_invoice_number = ''
    references = list()
    payment = Payment()
    delivery = Delivery()
    invoice_lines = list()  #: List[InvoiceLine]
    total_discount_amount = 0.0
    total_sales_amount = 0.0
    net_amount = 0.0
    tax_totals = list()  # List[TaxTotal]
    total_amount = 0.0
    extra_discount_amount = 0.0
    total_items_discount_amount = 0.0
    signatures = list()  #: List[Signature]

    def __init__(self):
        print('initializing a new Person object')

    @staticmethod
    def from_dict(obj: Any) -> 'Document':
        assert isinstance(obj, dict)
        issuer = Partner.from_dict(obj.get("issuer"))
        receiver = Partner.from_dict(obj.get("receiver"))
        document_type = from_str(obj.get("documentType"))
        document_type_version = from_str(obj.get("documentTypeVersion"))
        date_time_issued = from_str(obj.get("dateTimeIssued"))
        taxpayer_activity_code = from_str(obj.get("taxpayerActivityCode"))
        internal_id = from_str(obj.get("internalID"))
        purchase_order_reference = from_str(obj.get("purchaseOrderReference"))
        purchase_order_description = from_str(obj.get("purchaseOrderDescription"))
        sales_order_reference = from_str(obj.get("salesOrderReference"))
        sales_order_description = from_str(obj.get("salesOrderDescription"))
        proforma_invoice_number = from_str(obj.get("proformaInvoiceNumber"))
        references = from_list(from_str, obj.get("references"))
        payment = Payment.from_dict(obj.get("payment"))
        delivery = Delivery.from_dict(obj.get("delivery"))
        invoice_lines = from_list(InvoiceLine.from_dict, obj.get("invoiceLines"))
        total_discount_amount = from_float(obj.get("totalDiscountAmount"))
        total_sales_amount = from_float(obj.get("totalSalesAmount"))
        net_amount = from_float(obj.get("netAmount"))
        tax_totals = from_list(TaxTotal.from_dict, obj.get("taxTotals"))
        total_amount = from_float(obj.get("totalAmount"))
        extra_discount_amount = from_float(obj.get("extraDiscountAmount"))
        total_items_discount_amount = from_float(obj.get("totalItemsDiscountAmount"))
        signatures = from_list(Signature.from_dict, obj.get("signatures"))
        return Document(issuer, receiver, document_type, document_type_version, date_time_issued,
                        taxpayer_activity_code, internal_id, purchase_order_reference, purchase_order_description,
                        sales_order_reference, sales_order_description, proforma_invoice_number, references, payment,
                        delivery, invoice_lines, total_discount_amount, total_sales_amount, net_amount, tax_totals,
                        total_amount, extra_discount_amount, total_items_discount_amount, signatures)

    def to_dict(self) -> dict:
        result: dict = {}
        result["issuer"] = to_class(Partner, self.issuer)
        result["receiver"] = to_class(Partner, self.receiver)
        result["documentType"] = from_str(self.document_type)
        result["documentTypeVersion"] = from_str(self.document_type_version)
        result["dateTimeIssued"] = from_str(self.date_time_issued)
        result["taxpayerActivityCode"] = from_str(self.taxpayer_activity_code)
        result["internalID"] = from_str(self.internal_id)
        result["purchaseOrderReference"] = from_str(self.purchase_order_reference)
        result["purchaseOrderDescription"] = from_str(self.purchase_order_description)
        result["salesOrderReference"] = from_str(self.sales_order_reference)
        result["salesOrderDescription"] = from_str(self.sales_order_description)
        result["proformaInvoiceNumber"] = from_str(self.proforma_invoice_number)
        if self.document_type.upper() != 'I':
            result["references"] = from_list(from_str, self.references)
        result["payment"] = to_class(Payment, self.payment)
        result["delivery"] = to_class(Delivery, self.delivery)
        result["invoiceLines"] = from_list(lambda x: to_class(InvoiceLine, x), self.invoice_lines)
        result["totalDiscountAmount"] = to_float(self.total_discount_amount)
        result["totalSalesAmount"] = to_float(self.total_sales_amount)
        result["netAmount"] = to_float(self.net_amount)
        result["taxTotals"] = from_list(lambda x: to_class(TaxTotal, x), self.tax_totals)
        result["totalAmount"] = to_float(self.total_amount)
        result["extraDiscountAmount"] = to_float(self.extra_discount_amount)
        result["totalItemsDiscountAmount"] = to_float(self.total_items_discount_amount)
        result["signatures"] = from_list(lambda x: to_class(Signature, x), self.signatures)
        return result


@dataclass
class TaxesList:
    taxable_items: List[TaxableItem]

    @staticmethod
    def from_dict(obj: Any) -> 'TaxesList':
        assert isinstance(obj, dict)
        taxable_items = from_union([lambda x: from_list(TaxableItem.from_dict, x), from_none], obj.get("taxableItems"))
        return TaxesList(taxable_items)

    def to_dict(self) -> dict:
        result: dict = {}
        result["taxableItems"] = from_union([lambda x: from_list(lambda x: to_class(TaxableItem, x), x), from_none],
                                            self.taxable_items)
        return result


@dataclass
class DocData:
    documents = list()  #: List[Document]

    @staticmethod
    def from_dict(obj: Any) -> 'DocData':
        assert isinstance(obj, dict)
        documents = from_list(Document.from_dict, obj.get("documents"))
        return DocData(documents)

    def to_dict(self) -> dict:
        result: dict = {}
        result["documents"] = from_list(lambda x: to_class(Document, x), self.documents)
        return result


# def doc_data_from_dict(s: Any) -> DocData:
#     return DocData.from_dict(s)
#
#
# def doc_data_to_dict(x: DocData) -> Any:
#     return to_class(DocData, x)

@dataclass
class AcceptedDocument:
    uuid: str
    long_id: str
    internal_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'AcceptedDocument':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("uuid"))
        long_id = from_str(obj.get("longId"))
        internal_id = from_str(obj.get("internalId"))
        return AcceptedDocument(uuid, long_id, internal_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = from_str(self.uuid)
        result["longId"] = from_str(self.long_id)
        result["internalId"] = from_str(self.internal_id)
        return result


@dataclass
class Error:
    code: str
    message: str
    target: str
    details: Optional[List['Error']] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Error':
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        message = from_str(obj.get("message"))
        target = from_str(obj.get("target"))
        details = from_union([lambda x: from_list(Error.from_dict, x), from_none], obj.get("details"))
        return Error(code, message, target, details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        result["message"] = from_str(self.message)
        result["target"] = from_str(self.target)
        result["details"] = from_union([lambda x: from_list(lambda x: to_class(Error, x), x), from_none], self.details)
        return result


@dataclass
class RejectedDocument:
    internal_id: str
    error: Error

    @staticmethod
    def from_dict(obj: Any) -> 'RejectedDocument':
        assert isinstance(obj, dict)
        internal_id = from_str(obj.get("internalId"))
        error = Error.from_dict(obj.get("error"))
        return RejectedDocument(internal_id, error)

    def to_dict(self) -> dict:
        result: dict = {}
        result["internalId"] = from_str(self.internal_id)
        result["error"] = to_class(Error, self.error)
        return result


@dataclass
class SubmitResponse:
    submission_uuid: str
    accepted_documents: List[AcceptedDocument]
    rejected_documents: List[RejectedDocument]

    @staticmethod
    def from_dict(obj: Any) -> 'SubmitResponse':
        assert isinstance(obj, dict)
        submission_uuid = from_str(obj.get("submissionUUID"))
        accepted_documents = from_list(AcceptedDocument.from_dict, obj.get("acceptedDocuments"))
        rejected_documents = from_list(RejectedDocument.from_dict, obj.get("rejectedDocuments"))
        return SubmitResponse(submission_uuid, accepted_documents, rejected_documents)

    def to_dict(self) -> dict:
        result: dict = {}
        result["submissionUUID"] = from_str(self.submission_uuid)
        result["acceptedDocuments"] = from_list(lambda x: to_class(AcceptedDocument, x), self.accepted_documents)
        result["rejectedDocuments"] = from_list(lambda x: to_class(RejectedDocument, x), self.rejected_documents)
        return result


# endregion

# region Get Document
# https://sdk.invoicing.eta.gov.eg/api/12-get-document/#overview
@dataclass
class ValidationStep:
    name: str
    status: str
    error: Error

    @staticmethod
    def from_dict(obj: Any) -> 'ValidationStep':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        status = from_str(obj.get("status"))
        error = Error.from_dict(obj.get("error"))
        return ValidationStep(name, status, error)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["status"] = from_str(self.status)
        result["error"] = to_class(Error, self.error)
        return result


@dataclass
class ValidationResults:
    status: str
    validation_steps: List[ValidationStep]

    @staticmethod
    def from_dict(obj: Any) -> 'ValidationResults':
        assert isinstance(obj, dict)
        status = from_str(obj.get("status"))
        validation_steps = from_list(ValidationStep.from_dict, obj.get("validationSteps"))
        return ValidationResults(status, validation_steps)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = from_str(self.status)
        result["validationSteps"] = from_list(lambda x: to_class(ValidationStep, x), self.validation_steps)
        return result


@dataclass
class GetDocResponse:
    uuid: str
    submission_uuid: str
    long_id: str
    internal_id: str
    type_name: str
    type_version_name: str
    issuer_id: str
    issuer_name: str
    receiver_id: str
    receiver_name: str
    date_time_issued: str
    date_time_received: str
    total_sales: float
    total_discount: float
    net_amount: float
    total: float
    status: str
    document: Document
    transformation_status: str
    validation_results: ValidationResults

    @staticmethod
    def from_dict(obj: Any) -> 'GetDocResponse':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("uuid"))
        submission_uuid = from_str(obj.get("submissionUUID"))
        long_id = from_str(obj.get("longId"))
        internal_id = from_str(obj.get("internalId"))
        type_name = from_str(obj.get("typeName"))
        type_version_name = from_str(obj.get("typeVersionName"))
        issuer_id = from_str(obj.get("issuerId"))
        issuer_name = from_str(obj.get("issuerName"))
        receiver_id = from_str(obj.get("receiverId"))
        receiver_name = from_str(obj.get("receiverName"))
        date_time_issued = from_str(obj.get("dateTimeIssued"))
        date_time_received = from_str(obj.get("dateTimeReceived"))
        total_sales = from_float(obj.get("totalSales"))
        total_discount = from_float(obj.get("totalDiscount"))
        net_amount = from_float(obj.get("netAmount"))
        total = from_float(obj.get("total"))
        status = from_str(obj.get("status"))
        document = Document.from_dict(obj.get("document"))
        transformation_status = from_str(obj.get("transformationStatus"))
        validation_results = ValidationResults.from_dict(obj.get("validationResults"))
        return GetDocResponse(uuid, submission_uuid, long_id, internal_id, type_name, type_version_name, issuer_id,
                              issuer_name, receiver_id, receiver_name, date_time_issued, date_time_received,
                              total_sales, total_discount, net_amount, total, status, document, transformation_status,
                              validation_results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = from_str(self.uuid)
        result["submissionUUID"] = from_str(self.submission_uuid)
        result["longId"] = from_str(self.long_id)
        result["internalId"] = from_str(self.internal_id)
        result["typeName"] = from_str(self.type_name)
        result["typeVersionName"] = from_str(self.type_version_name)
        result["issuerId"] = from_str(self.issuer_id)
        result["issuerName"] = from_str(self.issuer_name)
        result["receiverId"] = from_str(self.receiver_id)
        result["receiverName"] = from_str(self.receiver_name)
        result["dateTimeIssued"] = from_str(self.date_time_issued)
        result["dateTimeReceived"] = from_str(self.date_time_received)
        result["totalSales"] = to_float(self.total_sales)
        result["totalDiscount"] = to_float(self.total_discount)
        result["netAmount"] = to_float(self.net_amount)
        result["total"] = to_float(self.total)
        result["status"] = from_str(self.status)
        result["document"] = to_class(Document, self.document)
        result["transformationStatus"] = from_str(self.transformation_status)
        result["validationResults"] = to_class(ValidationResults, self.validation_results)
        return result


# endregion

# region Get Document details
# https://sdk.invoicing.eta.gov.eg/api/20-get-document-details/
@dataclass
class GetDocDetailsResponse:
    long_id: str
    date_time_received: str
    status: str
    transformation_status: str
    cancel_request_date: str
    reject_request_date: str
    cancel_request_delayed_date: str
    reject_request_delayed_date: str
    decline_cancel_request_date: str
    decline_reject_request_date: str
    document: Document
    validation_results: ValidationResults

    @staticmethod
    def from_dict(obj: Any) -> 'GetDocDetailsResponse':
        assert isinstance(obj, dict)
        long_id = from_str(obj.get("longId"))
        date_time_received = from_str(obj.get("dateTimeReceived"))
        status = from_str(obj.get("status"))
        transformation_status = from_str(obj.get("transformationStatus"))
        cancel_request_date = from_str(obj.get("cancelRequestDate"))
        reject_request_date = from_str(obj.get("rejectRequestDate"))
        cancel_request_delayed_date = from_str(obj.get("cancelRequestDelayedDate"))
        reject_request_delayed_date = from_str(obj.get("rejectRequestDelayedDate"))
        decline_cancel_request_date = from_str(obj.get("declineCancelRequestDate"))
        decline_reject_request_date = from_str(obj.get("declineRejectRequestDate"))
        document = Document.from_dict(obj.get("document"))
        validation_results = ValidationResults.from_dict(obj.get("validationResults"))
        return GetDocDetailsResponse(long_id, date_time_received, status, transformation_status, cancel_request_date,
                                     reject_request_date, cancel_request_delayed_date, reject_request_delayed_date,
                                     decline_cancel_request_date, decline_reject_request_date, document,
                                     validation_results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["longId"] = from_str(self.long_id)
        result["dateTimeReceived"] = from_str(self.date_time_received)
        result["status"] = from_str(self.status)
        result["transformationStatus"] = from_str(self.transformation_status)
        result["cancelRequestDate"] = from_str(self.cancel_request_date)
        result["rejectRequestDate"] = from_str(self.reject_request_date)
        result["cancelRequestDelayedDate"] = from_str(self.cancel_request_delayed_date)
        result["rejectRequestDelayedDate"] = from_str(self.reject_request_delayed_date)
        result["declineCancelRequestDate"] = from_str(self.decline_cancel_request_date)
        result["declineRejectRequestDate"] = from_str(self.decline_reject_request_date)
        result["document"] = to_class(Document, self.document)
        result["validationResults"] = to_class(ValidationResults, self.validation_results)
        return result


# endregion

# region Get Recent
# https://sdk.invoicing.eta.gov.eg/api/08-get-recent-documents/
@dataclass
class MetadataResult:
    total_pages: int
    total_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'MetadataResult':
        assert isinstance(obj, dict)
        total_pages = from_int(obj.get("totalPages"))
        total_count = from_int(obj.get("totalCount"))
        return MetadataResult(total_pages, total_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["totalPages"] = from_int(self.total_pages)
        result["totalCount"] = from_int(self.total_count)
        return result


@dataclass
class DocumentSummary:
    uuid: str
    submission_uuid: str
    long_id: str
    internal_id: str
    type_name: str
    type_version_name: str
    issuer_id: str
    issuer_name: str
    receiver_id: str
    receiver_name: str
    date_time_issued: str
    date_time_received: str
    total_sales: float
    total_discount: float
    net_amount: float
    total: float
    status: str
    cancel_request_date: str
    reject_request_date: str
    cancel_request_delayed_date: str
    reject_request_delayed_date: str
    decline_cancel_request_date: str
    decline_reject_request_date: str

    @staticmethod
    def from_dict(obj: Any) -> 'DocumentSummary':
        assert isinstance(obj, dict)
        uuid = from_str(obj.get("uuid"))
        submission_uuid = from_str(obj.get("submissionUUID"))
        long_id = from_str(obj.get("longId"))
        internal_id = from_str(obj.get("internalId"))
        type_name = from_str(obj.get("typeName"))
        type_version_name = from_str(obj.get("typeVersionName"))
        issuer_id = from_str(obj.get("issuerId"))
        issuer_name = from_str(obj.get("issuerName"))
        receiver_id = from_str(obj.get("receiverId"))
        receiver_name = from_str(obj.get("receiverName"))
        date_time_issued = from_str(obj.get("dateTimeIssued"))
        date_time_received = from_str(obj.get("dateTimeReceived"))
        total_sales = from_float(obj.get("totalSales"))
        total_discount = from_float(obj.get("totalDiscount"))
        net_amount = from_float(obj.get("netAmount"))
        total = from_float(obj.get("total"))
        status = from_str(obj.get("status"))
        cancel_request_date = from_str(obj.get("cancelRequestDate"))
        reject_request_date = from_str(obj.get("rejectRequestDate"))
        cancel_request_delayed_date = from_str(obj.get("cancelRequestDelayedDate"))
        reject_request_delayed_date = from_str(obj.get("rejectRequestDelayedDate"))
        decline_cancel_request_date = from_str(obj.get("declineCancelRequestDate"))
        decline_reject_request_date = from_str(obj.get("declineRejectRequestDate"))
        return DocumentSummary(uuid, submission_uuid, long_id, internal_id, type_name, type_version_name, issuer_id,
                               issuer_name, receiver_id, receiver_name, date_time_issued, date_time_received,
                               total_sales, total_discount, net_amount, total, status, cancel_request_date,
                               reject_request_date, cancel_request_delayed_date, reject_request_delayed_date,
                               decline_cancel_request_date, decline_reject_request_date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = from_str(self.uuid)
        result["submissionUUID"] = from_str(self.submission_uuid)
        result["longId"] = from_str(self.long_id)
        result["internalId"] = from_str(self.internal_id)
        result["typeName"] = from_str(self.type_name)
        result["typeVersionName"] = from_str(self.type_version_name)
        result["issuerId"] = from_str(self.issuer_id)
        result["issuerName"] = from_str(self.issuer_name)
        result["receiverId"] = from_str(self.receiver_id)
        result["receiverName"] = from_str(self.receiver_name)
        result["dateTimeIssued"] = from_str(self.date_time_issued)
        result["dateTimeReceived"] = from_str(self.date_time_received)
        result["totalSales"] = to_float(self.total_sales)
        result["totalDiscount"] = to_float(self.total_discount)
        result["netAmount"] = to_float(self.net_amount)
        result["total"] = to_float(self.total)
        result["status"] = from_str(self.status)
        result["cancelRequestDate"] = from_str(self.cancel_request_date)
        result["rejectRequestDate"] = from_str(self.reject_request_date)
        result["cancelRequestDelayedDate"] = from_str(self.cancel_request_delayed_date)
        result["rejectRequestDelayedDate"] = from_str(self.reject_request_delayed_date)
        result["declineCancelRequestDate"] = from_str(self.decline_cancel_request_date)
        result["declineRejectRequestDate"] = from_str(self.decline_reject_request_date)
        return result


@dataclass
class GetRecentResponse:
    result: List[DocumentSummary]
    metadata: List[MetadataResult]

    @staticmethod
    def from_dict(obj: Any) -> 'GetRecentResponse':
        assert isinstance(obj, dict)
        result = from_list(DocumentSummary.from_dict, obj.get("result"))
        metadata = from_list(MetadataResult.from_dict, obj.get("metadata"))
        return GetRecentResponse(result, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["result"] = from_list(lambda x: to_class(DocumentSummary, x), self.result)
        result["metadata"] = from_list(lambda x: to_class(MetadataResult, x), self.metadata)
        return result
# endregion

# region

# endregion

# region
# endregion
