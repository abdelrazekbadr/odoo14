# # This code parses date/times, so please
# #
# #     pip install python-dateutil
# #
# # To use this code, make sure you
# #
# #     import json
# #
# # and then, to convert JSON from a string, do
# #
# #     result = doc_data_from_dict(json.loads(json_string))
# from ..api.documents import *
# from .utils import *
# from dataclasses import dataclass
# from datetime import datetime
# from typing import Any, List, Optional, TypeVar, Callable, Type, cast
# from . import *
# import dateutil.parser
# @dataclass
# class Delivery:
#     approach: Optional[str] = None
#     packaging: Optional[str] = None
#     date_validity: Optional[str] = None #change datetime to str
#     export_port: Optional[str] = None
#     country_of_orgin: Optional[str] = None
#     gross_weight: Optional[float] = None
#     net_weight: Optional[float] = None
#     terms: Optional[str] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Delivery':
#         assert isinstance(obj, dict)
#         approach = from_union([from_str, from_none], obj.get("approach"))
#         packaging = from_union([from_str, from_none], obj.get("packaging"))
#         date_validity = from_union([from_str, from_none], obj.get("dateValidity"))
#         export_port = from_union([from_str, from_none], obj.get("exportPort"))
#         country_of_orgin = from_union([from_str, from_none], obj.get("countryOfOrigin"))
#         gross_weight = from_union([from_float, from_none], obj.get("grossWeight"))
#         net_weight = from_union([from_float, from_none], obj.get("netWeight"))
#         terms = from_union([from_str, from_none], obj.get("terms"))
#         return Delivery(approach, packaging, date_validity, export_port, gross_weight,country_of_orgin, net_weight, terms)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["approach"] = from_union([from_str, from_none], self.approach)
#         result["packaging"] = from_union([from_str, from_none], self.packaging)
#         result["dateValidity"] = from_union([from_str, from_none], self.date_validity)
#         result["exportPort"] = from_union([from_str, from_none], self.export_port)
#         result["countryOfOrigin"] = from_union([from_str, from_none], self.country_of_orgin)
#         result["grossWeight"] = from_union([to_float, from_none], self.gross_weight)
#         result["netWeight"] = from_union([to_float, from_none], self.net_weight)
#         result["terms"] = from_union([from_str, from_none], self.terms)
#         return result
#
#
# @dataclass
# class Discount:
#     rate: Optional[float] = None
#     amount: Optional[float] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Discount':
#         assert isinstance(obj, dict)
#         rate = from_union([from_float, from_none], obj.get("rate"))
#         amount = from_union([from_float, from_none], obj.get("amount"))
#         return Discount(rate, amount)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["rate"] = from_union([from_float, from_none], self.rate)
#         result["amount"] = from_union([from_float, from_none], self.amount)
#         return result
#
#
# @dataclass
# class TaxableItem:
#     tax_type: Optional[str] = None
#     amount: Optional[float] = None
#     sub_type: Optional[str] = None
#     rate: Optional[float] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'TaxableItem':
#         assert isinstance(obj, dict)
#         tax_type = from_union([from_str, from_none], obj.get("taxType"))
#         amount = from_union([from_float, from_none], obj.get("amount"))
#         sub_type = from_union([from_str, from_none], obj.get("subType"))
#         rate = from_union([from_float, from_none], obj.get("rate"))
#         return TaxableItem(tax_type, amount, sub_type, rate)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["taxType"] = from_union([from_str, from_none], self.tax_type)
#         result["amount"] = from_union([from_float, from_none], self.amount)
#         result["subType"] = from_union([from_str, from_none], self.sub_type)
#         result["rate"] = from_union([from_float, from_none], self.rate)
#         return result
#
#
# @dataclass
# class UnitValue:
#     currency_sold: Optional[str] = None
#     amount_egp: Optional[float] = None
#
#     amount_sold: Optional[float] = None
#     currency_exchangeRate: Optional[float] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'UnitValue':
#         assert isinstance(obj, dict)
#         currency_sold = from_union([from_str, from_none], obj.get("currencySold"))
#         amount_egp = from_union([from_float, from_none], obj.get("amountEGP"))
#
#         amount_sold: from_union([from_float, from_none], obj.get("amountSold"))
#         currency_exchangeRate: from_union([from_float, from_none], obj.get("currencyExchangeRate"))
#         return UnitValue(currency_sold, amount_egp.amount_sold,currency_exchangeRate)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["currencySold"] = from_union([from_str, from_none], self.currency_sold)
#         result["amountEGP"] = from_union([from_float, from_none], self.amount_egp)
#         result["amountSold"]= from_union([from_float, from_none], self.amount_sold)
#         result["currencyExchangeRate"]= from_union([from_float, from_none], self.currency_exchangeRate)
#         return result
#
#
# @dataclass
# class InvoiceLine:
#     description: Optional[str] = None
#     item_type: Optional[str] = None
#     item_code: Optional[str] = None
#     unit_type: Optional[str] = None
#     quantity: Optional[float] = None
#     internal_code: Optional[str] = None
#     sales_total: Optional[float] = None
#     total: Optional[float] = None
#     value_difference: Optional[float] = None
#     total_taxable_fees: Optional[float] = None
#     net_total: Optional[float] = None
#     items_discount: Optional[float] = None
#     unit_value: Optional[UnitValue] = None
#     discount: Optional[Discount] = None
#     taxable_items: Optional[List[TaxableItem]] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'InvoiceLine':
#         assert isinstance(obj, dict)
#         description = from_union([from_str, from_none], obj.get("description"))
#         item_type = from_union([from_str, from_none], obj.get("itemType"))
#         item_code = from_union([from_str, from_none], obj.get("itemCode"))
#         unit_type = from_union([from_str, from_none], obj.get("unitType"))
#         quantity = from_union([from_float, from_none], obj.get("quantity"))
#         internal_code = from_union([from_str, from_none], obj.get("internalCode"))
#         sales_total = from_union([from_float, from_none], obj.get("salesTotal"))
#         total = from_union([from_float, from_none], obj.get("total"))
#         value_difference = from_union([from_float, from_none], obj.get("valueDifference"))
#         total_taxable_fees = from_union([from_float, from_none], obj.get("totalTaxableFees"))
#         net_total = from_union([from_float, from_none], obj.get("netTotal"))
#         items_discount = from_union([from_float, from_none], obj.get("itemsDiscount"))
#         unit_value = from_union([UnitValue.from_dict, from_none], obj.get("unitValue"))
#         discount = from_union([Discount.from_dict, from_none], obj.get("discount"))
#         taxable_items = from_union([lambda x: from_list(TaxableItem.from_dict, x), from_none], obj.get("taxableItems"))
#         return InvoiceLine(description, item_type, item_code, unit_type, quantity, internal_code, sales_total, total, value_difference, total_taxable_fees, net_total, items_discount, unit_value, discount, taxable_items)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         try:
#             result["description"] = from_union([from_str, from_none], self.description)
#             result["itemType"] = from_union([from_str, from_none], self.item_type)
#             result["itemCode"] = from_union([from_str, from_none], self.item_code)
#             result["unitType"] = from_union([from_str, from_none], self.unit_type)
#             result["quantity"] = from_union([from_float, from_none], self.quantity)
#             result["internalCode"] = from_union([from_str, from_none], self.internal_code)
#             result["salesTotal"] = from_union([from_float, from_none], self.sales_total)
#             result["total"] = from_union([from_float, from_none], self.total)
#             result["valueDifference"] = from_union([from_float, from_none], self.value_difference)
#             result["totalTaxableFees"] = from_union([from_float, from_none], self.total_taxable_fees)
#             result["netTotal"] = from_union([from_float, from_none], self.net_total)
#             result["itemsDiscount"] = from_union([from_float, from_none], self.items_discount)
#             result["unitValue"] = from_union([lambda x: to_class(UnitValue, x), from_none], self.unit_value)
#             result["discount"] = from_union([lambda x: to_class(Discount, x), from_none], self.discount)
#             result["taxableItems"] = from_union([lambda x: from_list(lambda x: to_class(TaxableItem, x), x), from_none], self.taxable_items)
#         except Exception as ex:
#             print(ex)
#         return result
#
#
# @dataclass
# class Address:
#     branch_id: Optional[str] = None
#     country: Optional[str] = None
#     governate: Optional[str] = None
#     region_city: Optional[str] = None
#     street: Optional[str] = None
#     building_number: Optional[str] = None
#     postal_code: Optional[str] = None
#     floor: Optional[str] = None
#     room: Optional[str] = None
#     landmark: Optional[str] = None
#     additional_information: Optional[str] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Address':
#         assert isinstance(obj, dict)
#         branch_id = from_union([from_str, from_none], obj.get("branchID"))
#         country = from_union([from_str, from_none], obj.get("country"))
#         governate = from_union([from_str, from_none], obj.get("governate"))
#         region_city = from_union([from_str, from_none], obj.get("regionCity"))
#         street = from_union([from_str, from_none], obj.get("street"))
#         building_number = from_union([from_str, from_none], obj.get("buildingNumber"))
#         postal_code = from_union([from_str, from_none], obj.get("postalCode"))
#         floor = from_union([from_str, from_none], obj.get("floor"))
#         room = from_union([from_str, from_none], obj.get("room"))
#         landmark = from_union([from_str, from_none], obj.get("landmark"))
#         additional_information = from_union([from_str, from_none], obj.get("additionalInformation"))
#         return Address(branch_id, country, governate, region_city, street, building_number, postal_code, floor, room, landmark, additional_information)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["branchID"] = from_union([from_str, from_none], self.branch_id)
#         result["country"] = from_union([from_str, from_none], self.country)
#         result["governate"] = from_union([from_str, from_none], self.governate)
#         result["regionCity"] = from_union([from_str, from_none], self.region_city)
#         result["street"] = from_union([from_str, from_none], self.street)
#         result["buildingNumber"] = from_union([from_str, from_none], self.building_number)
#         result["postalCode"] = from_union([from_str, from_none], self.postal_code)
#         result["floor"] = from_union([from_str, from_none], self.floor)
#         result["room"] = from_union([from_str, from_none], self.room)
#         result["landmark"] = from_union([from_str, from_none], self.landmark)
#         result["additionalInformation"] = from_union([from_str, from_none], self.additional_information)
#         return result
#
#
# @dataclass
# class Partner:
#     address: Optional[Address] = None
#    type: #Optional[str] = None
#     id: Optional[str] = None
#     name: Optional[str] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Partner':
#         assert isinstance(obj, dict)
#         address = from_union([Address.from_dict, from_none], obj.get("address"))
#         type = from_union([from_str, from_none], obj.get("type"))
#         id = from_union([from_str, from_none], obj.get("id"))
#         name = from_union([from_str, from_none], obj.get("name"))
#         return Partner(address, type, id, name)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["address"] = from_union([lambda x: to_class(Address, x), from_none], self.address)
#         result["type"] = from_union([from_str, from_none], self.type)
#         result["id"] = from_union([from_str, from_none], self.id)
#         result["name"] = from_union([from_str, from_none], self.name)
#         return result
#
#
# @dataclass
# class Payment:
#     bank_name: Optional[str] = None
#     bank_address: Optional[str] = None
#     bank_account_no: Optional[str] = None
#     bank_account_iban: Optional[str] = None
#     swift_code: Optional[str] = None
#     terms: Optional[str] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Payment':
#         assert isinstance(obj, dict)
#         bank_name = from_union([from_str, from_none], obj.get("bankName"))
#         bank_address = from_union([from_str, from_none], obj.get("bankAddress"))
#         bank_account_no = from_union([from_str, from_none], obj.get("bankAccountNo"))
#         bank_account_iban = from_union([from_str, from_none], obj.get("bankAccountIBAN"))
#         swift_code = from_union([from_str, from_none], obj.get("swiftCode"))
#         terms = from_union([from_str, from_none], obj.get("terms"))
#         return Payment(bank_name, bank_address, bank_account_no, bank_account_iban, swift_code, terms)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["bankName"] = from_union([from_str, from_none], self.bank_name)
#         result["bankAddress"] = from_union([from_str, from_none], self.bank_address)
#         result["bankAccountNo"] = from_union([from_str, from_none], self.bank_account_no)
#         result["bankAccountIBAN"] = from_union([from_str, from_none], self.bank_account_iban)
#         result["swiftCode"] = from_union([from_str, from_none], self.swift_code)
#         result["terms"] = from_union([from_str, from_none], self.terms)
#         return result
#
#
# @dataclass
# class Signature:
#     signature_type: Optional[str] = None
#     value: Optional[str] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Signature':
#         assert isinstance(obj, dict)
#         signature_type = from_union([from_str, from_none], obj.get("signatureType"))
#         value = from_union([from_str, from_none], obj.get("value"))
#         return Signature(signature_type, value)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["signatureType"] = from_union([from_str, from_none], self.signature_type)
#         result["value"] = from_union([from_str, from_none], self.value)
#         return result
#
#
# @dataclass
# class TaxTotal:
#     tax_type: Optional[str] = None
#     amount: Optional[float] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'TaxTotal':
#         assert isinstance(obj, dict)
#         tax_type = from_union([from_str, from_none], obj.get("taxType"))
#         amount = from_union([from_float, from_none], obj.get("amount"))
#         return TaxTotal(tax_type, amount)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["taxType"] = from_union([from_str, from_none], self.tax_type)
#         result["amount"] = from_union([from_float, from_none], self.amount)
#         return result
#
#
# @dataclass
# class Document:
#     taxpayer_activity_code: Optional[str] = None
#     sales_order_reference: Optional[str] = None
#     issuer: Optional[Partner] = None
#     receiver: Optional[Partner] = None
#     document_type: Optional[str] = None
#     document_type_version: Optional[str] = None
#     date_time_issued: Optional[str] = None
#     internal_id: Optional[str] = None
#     purchase_order_reference: Optional[str] = None
#     purchase_order_description: Optional[str] = None
#     sales_order_description: Optional[str] = None
#     proforma_invoice_number: Optional[str] = None
#     payment: Optional[Payment] = None
#     delivery: Optional[Delivery] = None
#     invoice_lines: Optional[List[InvoiceLine]] = None
#     total_discount_amount: Optional[float] = None
#     total_sales_amount: Optional[float] = None
#     net_amount: Optional[float] = None
#     tax_totals: Optional[List[TaxTotal]] = None
#     total_amount: Optional[float] = None
#     extra_discount_amount: Optional[float] = None
#     total_items_discount_amount: Optional[float] = None
#     signatures: Optional[List[Signature]] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'Document':
#         assert isinstance(obj, dict)
#         taxpayer_activity_code = from_union([from_str, from_none], obj.get("taxpayerActivityCode"))
#         sales_order_reference = from_union([from_str, from_none], obj.get("salesOrderReference"))
#         issuer = from_union([Partner.from_dict, from_none], obj.get("issuer"))
#         receiver = from_union([Partner.from_dict, from_none], obj.get("receiver"))
#         document_type = from_union([from_str, from_none], obj.get("documentType"))
#         document_type_version = from_union([from_str, from_none], obj.get("documentTypeVersion"))
#         date_time_issued = from_union([from_str, from_none], obj.get("dateTimeIssued"))
#         internal_id = from_union([from_str, from_none], obj.get("internalID"))
#         purchase_order_reference = from_union([from_str, from_none], obj.get("purchaseOrderReference"))
#         purchase_order_description = from_union([from_str, from_none], obj.get("purchaseOrderDescription"))
#         sales_order_description = from_union([from_str, from_none], obj.get("salesOrderDescription"))
#         proforma_invoice_number = from_union([from_str, from_none], obj.get("proformaInvoiceNumber"))
#         payment = from_union([Payment.from_dict, from_none], obj.get("payment"))
#         delivery = from_union([Delivery.from_dict, from_none], obj.get("delivery"))
#         invoice_lines = from_union([lambda x: from_list(InvoiceLine.from_dict, x), from_none], obj.get("invoiceLines"))
#         total_discount_amount = from_union([from_str, from_none], obj.get("totalDiscountAmount"))
#         total_sales_amount = from_union([from_str, from_none], obj.get("totalSalesAmount"))
#         net_amount = from_union([from_str, from_none], obj.get("netAmount"))
#         tax_totals = from_union([lambda x: from_list(TaxTotal.from_dict, x), from_none], obj.get("taxTotals"))
#         total_amount = from_union([from_str, from_none], obj.get("totalAmount"))
#         extra_discount_amount = from_union([from_str, from_none], obj.get("extraDiscountAmount"))
#         total_items_discount_amount = from_union([from_str, from_none], obj.get("totalItemsDiscountAmount"))
#         signatures = from_union([lambda x: from_list(Signature.from_dict, x), from_none], obj.get("signatures"))
#         return Document(taxpayer_activity_code, sales_order_reference, issuer, receiver, document_type, document_type_version, date_time_issued, internal_id, purchase_order_reference, purchase_order_description, sales_order_description, proforma_invoice_number, payment, delivery, invoice_lines, total_discount_amount, total_sales_amount, net_amount, tax_totals, total_amount, extra_discount_amount, total_items_discount_amount, signatures)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         try:
#             result["taxpayerActivityCode"] = from_union([from_str, from_none], self.taxpayer_activity_code)
#             result["salesOrderReference"] = from_union([from_str, from_none], self.sales_order_reference)
#             result["issuer"] = from_union([lambda x: to_class(Partner, x), from_none], self.issuer)
#             result["receiver"] = from_union([lambda x: to_class(Partner, x), from_none], self.receiver)
#             result["documentType"] = from_union([from_str, from_none], self.document_type)
#             result["documentTypeVersion"] = from_union([from_str, from_none], self.document_type_version)
#             result["dateTimeIssued"] = from_union([from_str, from_none], self.date_time_issued)
#             result["internalID"] = from_union([from_str, from_none], self.internal_id)
#             result["purchaseOrderReference"] = from_union([from_str, from_none], self.purchase_order_reference)
#             result["purchaseOrderDescription"] = from_union([from_str, from_none], self.purchase_order_description)
#             result["salesOrderDescription"] = from_union([from_str, from_none], self.sales_order_description)
#             result["proformaInvoiceNumber"] = from_union([from_str, from_none], self.proforma_invoice_number)
#             result["payment"] = from_union([lambda x: to_class(Payment, x), from_none], self.payment)
#             result["delivery"] = from_union([lambda x: to_class(Delivery, x), from_none], self.delivery)
#             result["invoiceLines"] = from_union([lambda x: from_list(lambda x: to_class(InvoiceLine, x), x), from_none], self.invoice_lines)
#             result["totalDiscountAmount"] = from_union([from_float, from_none], self.total_discount_amount)
#             result["totalSalesAmount"] = from_union([from_float, from_none], self.total_sales_amount)
#             result["netAmount"] = from_union([from_float, from_none], self.net_amount)
#             result["taxTotals"] = from_union([lambda x: from_list(lambda x: to_class(TaxTotal, x), x), from_none], self.tax_totals)
#             result["totalAmount"] = from_union([from_float, from_none], self.total_amount)
#             result["extraDiscountAmount"] = from_union([from_float, from_none], self.extra_discount_amount)
#             result["totalItemsDiscountAmount"] = from_union([from_float, from_none], self.total_items_discount_amount)
#             result["signatures"] = from_union([lambda x: from_list(lambda x: to_class(Signature, x), x), from_none], self.signatures)
#         except Exception as ex:
#             print(ex)
#         return result
#
# @dataclass
# class TaxesList:
#     taxable_items: Optional[List[TaxableItem]] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'TaxesList':
#         assert isinstance(obj, dict)
#         taxable_items = from_union([lambda x: from_list(TaxableItem.from_dict, x), from_none], obj.get("taxableItems"))
#         return TaxesList(taxable_items)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["taxableItems"] = from_union([lambda x: from_list(lambda x: to_class(TaxableItem, x), x), from_none], self.taxable_items)
#         return result
#
#
# @dataclass
# class DocData:
#     documents: Optional[List[Document]] = None
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'DocData':
#         assert isinstance(obj, dict)
#         documents = from_union([lambda x: from_list(Document.from_dict, x), from_none], obj.get("documents"))
#         return DocData(documents)
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         result["documents"] = from_union([lambda x: from_list(lambda x: to_class(Document, x), x), from_none], self.documents)
#         return result
#
#
# def doc_data_from_dict(s: Any) -> DocData:
#     return DocData.from_dict(s)
#
#
# def doc_data_to_dict(x: DocData) -> Any:
#     return to_class(DocData, x)
