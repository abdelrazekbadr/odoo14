# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json

import requests
import logging
# import pydantic
from odoo import api, fields, models, tools, _, http
from odoo.http import request, serialize_exception
from ..api.documents import *

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EInvAPI(models.AbstractModel):
    _name = "egtax.einv_api"
    _description = "Eg E-Invoice API "

    api_version = "v1"
    api_version_number = "1.0"
    api_country_code = "EG"
    api_url_token = "/connect/token"
    api_url_submit_doc = f"/api/{api_version}/documentsubmissions"

    client_id = ""
    client_secret = ""
    apiBaseUrl = ""
    idSrvBaseUrl = ""
    auto_post = False
    token = ""

    #Configuration Key
    key_client_id = 'egtax.client_id'
    key_client_secret = 'egtax.client_secret'
    key_apiBaseUrl = 'egtax.apiBaseUrl'
    key_idSrvBaseUrl = 'egtax.idSrvBaseUrl'
    key_auto_post = 'egtax.auto_post'
    key_activity_code = 'egtax.activity_code'
    key_product_coding_schema= 'egtax.product_coding_schema'
    key_signature_type = 'egtax.signature_type'
    key_signature_value = 'egtax.signature_value'

    # def __init__(self, pool, cr):
    #     """ Override of __init__ to add access rights on livechat_username
    #         Access rights are disabled by default, but allowed
    #         on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
    #     """
    #     init_res = super(EInvAPI, self).__init__(pool, cr)
    #     config = self.env['ir.config_parameter'].sudo()
    #     self.client_id = config.get_param('egtax.client_id')
    #     self.client_secret = config.get_param('egtax.client_secret')
    #     self.apiBaseUrl = config.get_param('egtax.apiBaseUrl')
    #     self.idSrvBaseUrl = config.get_param('egtax.idSrvBaseUrl')
    #     self.auto_post = bool(config.get_param('egtax.auto_post'))
    #
    #     return  init_res
    #
    def load_config(self):
        config = self.env['ir.config_parameter'].sudo()
        self.client_id = config.get_param('egtax.client_id')
        self.client_secret = config.get_param('egtax.client_secret')
        self.apiBaseUrl = config.get_param('egtax.apiBaseUrl')
        self.idSrvBaseUrl = config.get_param('egtax.idSrvBaseUrl')
        self.auto_post = bool(config.get_param('egtax.auto_post'))

    def get_config(self,key):
        config = self.env['ir.config_parameter'].sudo()
        return  config.get_param(key)

    # def submit_documents(self):
    @api.model
    def api_submit_documents(self):
        """
        submit documents
        """
        url = f"{self.apiBaseUrl}{self.api_url_submit_doc}"
        payload=self.get_doc_payload()
        g = ""

        # try:
        #     headers = {'Content-Type': 'application/json','Authorization':f'bearer {self.token}'}
        #     #params = {'format': 'json', 'q': addr}
        #     response = requests.get("POST",url, headers=headers,data=payload)
        #     _logger.info(f'{url} called')
        #     if response.status_code != 200:
        #         _logger.error('Request to openstreetmap failed.\nCode: %s\nContent: %s' % (response.status_code, response.content))
        #     result = response.json()
        # except Exception as e:
        #     self._raise_query_error(e)
        #

    def get_doc_payload(self):
        docs_ids = self.env.context.get('active_ids', [])
        if len(self) == 1:
            docs_ids.append(self.id)
        docs = DocData()
        docs.documents = list()
        selected_records = self.env['account.move'].browse(docs_ids)

        for invoice in selected_records:
            doc = self.map_doc(invoice)
            # Issuer
            doc.issuer = self.map_partner(self.env.company.partner_id)
            # Receiver
            doc.receiver = self.map_partner(invoice.partner_id)

            # Refererences

            # Payment
            doc.payment = self.map_payment(invoice)

            # Delivery
            doc.delivery = self.map_delivery(invoice)

            # Invoice lines

            doc.invoice_lines = self.map_invoice_lines(invoice)

            doc.tax_totals = self.map_tax_totals(doc.invoice_lines)  # Totals per tax type

            # Signatures
            doc.signatures = self.map_signatures()

            docs.documents.append(doc)

        payload = docs.to_dict()

        return payload

    # return with e-invoice api standard structure -------------------
    def map_doc(self, invoice) -> 'Document':
        doc = Document()
        # invoice
        if invoice.move_type == 'out_invoice':
            doc.document_type = "i"

        elif invoice.move_type == 'out_refund': # Credit Note#Customer Return
            doc.document_type = "c"

        elif invoice.move_type == 'in_refund':  # Debit Note#Vendor Return
            doc.document_type = "d"


        doc.document_type_version = self.api_version_number

        # https://www.programiz.com/python-programming/datetime/strftime
        doc.date_time_issued =  invoice.invoice_date.strftime('%Y-%m-%dT%H:%M:%SZ') if invoice.invoice_date else ''

        doc.taxpayer_activity_code =self.get_config(self.key_activity_code) or ''
        doc.internal_id = invoice.name
        doc.purchase_order_reference = ""  # Optional if enable purchase module
        doc.purchase_order_description = ""  # Optional if enable purchase module
        doc.sales_order_reference = ""  # Optional if enable sale module
        doc.sales_order_description = ""  # Optional if enable sale module
        doc.proforma_invoice_number = ""  # Optional: Reference to the previous proforma invoice.

        #Totals
        doc.total_discount_amount =self.compute_total_discount_amount(invoice)  # ToDo: Review total_discount_amount
         #Total amount of discounts: sum of all Discount amount elements of InvoiceLine items.

        doc.total_sales_amount = invoice.amount_untaxed+doc.total_discount_amount  #ToDo: Review total_discount_amount
        #Sum all all InvoiceLine/SalesTotal items

        doc.net_amount = invoice.amount_untaxed
        #TotalSales – TotalDiscount

        doc.extra_discount_amount = 0.0  # ToDo: when add_new
        #Additional discount amount applied at the level of the overall document, not individual lines.

        doc.total_items_discount_amount =doc.extra_discount_amount+doc.total_discount_amount
        #Total amount of item discounts: sum of all Item Discount amount elements of InvoiceLine items.

        doc.total_amount = invoice.amount_total  # ToDo: Review total_amount
        #Total amount of the invoice calculated as NetAmount + Totals of tax amounts. 5 decimal digits allowed.

        return doc

    def map_partner(self, res_partner) -> 'Partner':
        partner = Partner()
        # Basic info
        partner.id = res_partner.vat  # Registeration Number or Nationl ID
        partner.name = res_partner.name or ""
        partner.type = 'B' if res_partner.is_company else 'P'
        if res_partner.country_id.code != None and res_partner.country_id.code != self.api_country_code:
            partner.type = 'F'

        # Address
        partner.address = Address()
        partner.address.branch_id = "" or ""  # ToDo:Add in setting
        # or add app: https://apps.odoo.com/apps/modules/14.0/boraq_company_branches/

        partner.address.country = res_partner.country_id.code or ""
        partner.address.governate = res_partner.state_id.name or ""
        partner.address.region_city = res_partner.city or ""
        partner.address.street = res_partner.street or ""
        partner.address.building_number = res_partner.street2 or ""  # working as building number
        partner.address.postal_code = res_partner.zip or ""  # optional
        partner.address.floor = "" or ""  # optional
        partner.address.room = "" or ""  # optional
        partner.address.landmark = "" or ""  # optional
        partner.address.additional_information = "" or ""  # optional

        # self.env.company
        return partner

    def map_payment(self, invoice) -> 'Payment':
        # Payment
        payment = Payment()
        payment.bank_name = ""
        payment.bank_account_no = ""
        payment.bank_address = ""
        payment.bank_account_iban = ""
        payment.swift_code = ""
        payment.terms = ""
        return payment

    def map_delivery(self, invoice) -> 'Delivery':
        # Delivery
        delivery = Delivery()
        delivery.approach = ""
        delivery.date_validity = ""
        delivery.export_port = ""
        delivery.packaging = ""
        delivery.country_of_orgin = ""
        delivery.gross_weight = 0.0
        delivery.net_weight = 0.0
        delivery.terms = ""
        return delivery

    def map_invoice_lines(self, invoice):
        lines = list()
        for line in invoice.invoice_line_ids:
            newLine = InvoiceLine()
            newLine.description = line.name
            #GS1 Egypt https://gs1eg.org/
            #GS1 SA https://www.gs1.org.sa/
            newLine.item_type = self.get_config(self.key_product_coding_schema) or 'GS1' #
            # Must be GS1 or EGS for this version.

            newLine.item_code = line.product_id.barcode or ""
            #Code of the goods or services item being sold. GS1 codes targeted for managing goods,
            # EGS codes targeted for managing goods – goods or services.

            newLine.unit_type = line.product_uom_id.einv_code or '' #TODO:Review unit_type .
            newLine.quantity = line.quantity #Number of units of the defined unit type being sold. Number should be larger than 0.
            newLine.internal_code = line.product_id.default_code or ""
            newLine.sales_total = line.quantity*line.price_unit #Total amount for the invoice line considering quantity and unit price in EGP
            # (with excluded factory amounts if they are present for specific types in documents).

            newLine.total =line.price_total #Total amount for the invoice line after
            # adding all pricing items, taxes, removing discounts.

            newLine.value_difference = 0
            #Value difference when selling goods already taxed (accepts +/- numbers),
            # e.g., factory value based.

            newLine.total_taxable_fees = 0#Total amount of additional taxable fees to be used in final tax calculation.
            newLine.net_total = line.price_subtotal # Total amount for the invoice line after applying discount.
            newLine.items_discount = 0 # Non-taxable items discount.

            # unit_value: #	The structure defining the price of a single unit sold.
            newLine.unit_value =UnitValue()
            newLine.unit_value.currency_sold = line.currency_id.name
            newLine.unit_value.currency_exchangeRate = 1.0  #
            newLine.unit_value.amount_egp = line.price_unit * newLine.unit_value.currency_exchangeRate
            newLine.unit_value.amount_sold = line.price_unit

            # newLine.discount: # Optional: the structure defining the discount applied on a single unit sold.
            newLine.discount=Discount(rate=line.discount,amount=line.price_unit*line.discount/100)

            # newLine.taxable_items: #Optional: List of taxable items. Can have zero or more of supported tax items
            # below from the list of all tax types including VAT, WHT and table tax, local authority fees (municipality), development.
            newLine.taxable_items=list()
            for tax in line.tax_ids:
                tax_item=TaxableItem()
                tax_item.tax_type=tax.einv_code or 'T12'#tax.type_tax_use #
                #Type of tax applied - from the list of approved tax type codes.
                # The TaxType needs to be unique across the invoice line (no VAT twice in one invoice line),
                # TaxType is from the list of supported tax types.
                # https: // sdk.invoicing.eta.gov.eg / codes / tax - types /

                tax_item.amount=tax.amount if tax.amount_type=='fixed' \
                    else line.price_subtotal* tax.amount/100 if tax.amount_type=='percent'  else 0
                #Amount of the tax applied – tax type defined type of tax applies to support different taxes
                # that are possible depending on the type of sales, customer etc. Value with the precision of 2

                tax_item.sub_type=tax.einv_sub_code or '' #
                #Subtype of the tax type that might mean exemption rate is applied or
                # specific rate linked to product type being sold is applied.

                tax_item.rate=tax.amount if tax.amount_type=='percent' else 0 # Tax rate applied for the invoice line. Value from 0 to 100.

                newLine.taxable_items.append(tax_item)

            lines.append(newLine)


        return lines

    def map_tax_totals(self, invoice_lines):
        # https://sdk.invoicing.eta.gov.eg/codes/tax-types/

        #flatten nested taxes list
        taxes_lines = [item for sublist in ([line.taxable_items for line in invoice_lines])
                       for item in sublist]

        if taxes_lines and len(taxes_lines)>0:
            taxable_items_dict = TaxesList(taxable_items=taxes_lines).to_dict()
            taxes_groups = sum_group_by(taxable_items_dict["taxableItems"], "taxType", ["amount"])

            tax_totals = [TaxTotal(tax_type=g,amount=taxes_groups[g]['amount']) for g in taxes_groups]
            return tax_totals

        else:
            return list()

        # tax_type
        # Type of tax applied - from the list of approved tax type codes.
        # The TaxType needs to be unique across the invoice line (no VAT twice in one invoice line),
        # TaxType is from the list of supported tax types

        #amount =
        # Sum of all amounts of given tax in all invoice lines. 5 decimal digits allowed.

    def compute_total_discount_amount(self,invoice)->'float':

        #self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        #sum(line.price_unit * line.quantity for line in invoice.invoice_line_ids)
        total_before_discount_unit = sum(line.price_unit * line.quantity for line in invoice.invoice_line_ids)
        total_discount_amount=total_before_discount_unit - invoice.amount_untaxed

        return total_discount_amount

    def map_signatures(self):
        # Read from config setting
        signatures = list()

        #1
        signature = Signature()
        signature.signature_type = self.get_config(self.key_signature_type) or "i"
        signature.value = self.get_config(self.key_signature_value) or ""
        signatures.append(signature)

        #2 - if another signature
        return signatures



class EgtaxApiController(http.Controller):

    @http.route('/web/einv/api/doc/download/<string:res_model>/<int:res_id>', type='http', auth="public")
    #@serialize_exception
    def download_doc(self, res_model, res_id,):
        """
        """
        docs_dict = self.get_doc_payload()
        body = json.dumps(docs_dict)
        request.disable_db = False
        response = request.make_response(body, [
            # this method must specify a content-type application/json instead of using the default text/html set because
            # the type of the route is set to HTTP, but the rpc is made with a get and expects JSON
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'public, max-age=' + str(http.STATIC_CACHE_LONG))])
        return response

