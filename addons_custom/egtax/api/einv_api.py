# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from base64 import b64encode
from odoo.addons.egtax.enums.config_keys import ConfigKeys
import requests
import logging
# import pydantic
from odoo import api, fields, models, tools, _, http
from odoo.http import request, serialize_exception
from ..api.documents import *
from datetime import datetime, timedelta

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

    # PUT /api/v1.0/documents/{UUID}/state

    def get_config(self, key):
        config = self.env['ir.config_parameter'].sudo()
        return config.get_param(key)

    def set_config(self, key, value):
        self.env['ir.config_parameter'].sudo().set_param(key, value)

    # region helper methods
    def validate_token(self):
        # check expire 1 hour by default after called token
        token_date_text = self.get_config(ConfigKeys.CLIENT_TOKEN_LAST_DATE.value)
        token = self.get_config(ConfigKeys.CLIENT_TOKEN.value)
        if token_date_text:
            token_date = dateutil.parser.parse(token_date_text)
            expire_in = int(self.get_config(ConfigKeys.CLIENT_TOKEN_EXPIRE_IN.value) or '0')
            seconds_to_validate = expire_in - 60 if expire_in > 1800 else expire_in - 1  # for safty session
            expire_in_date = token_date + timedelta(seconds=seconds_to_validate)

            if datetime.now() < expire_in_date and token:
                return token
            else:
                return self.api_auth()  # auth again if expire or token empty
        else:
            return self.api_auth()  # auth if first time

    def _raise_query_error(self, error):
        raise UserError(_('API e-Invoice Error:') + ' %s' % error)

    def write_log_all(self, response):
        result = response.json()
        docs_ids = self.env.context.get('active_ids', [])
        if len(self) == 1:
            docs_ids = [self.id]
            # docs_ids.append(self.id)

        err_name = result.get("error") or result.get("code") or ''
        err_code = result.get("code") or result.get("error") or response.status_code or ''
        err_msg = result.get("message") or result.get("error_description") or ''
        err_target = result.get("target") or ''
        err_uri = result.get("error_uri") or ''

        error = Error(code=err_code, message=err_msg, target=err_target, details=list())
        error.err_uri = err_uri
        error.err_name = err_name

        selected_records = self.env['account.move'].browse(docs_ids)

        for invoice in selected_records:
            self.write_log(invoice, error)

    def write_log(self, invoice, error):
        invoice.einv_error_code = error.code
        invoice.einv_error_message = error.message
        # handle error error,error_description,error_uri
        self.write_error_details(invoice, error)
        if error.details:
            for err in error.details:
                self.write_error_details(invoice, err)

    def write_error_details(self, invoice, error):
        invoice.write({'errors_detail_ids':
                           [(0, 0,
                             {
                                 'name': error.name or error.code or '',  # optional
                                 'code': error.code or '',
                                 'message': error.message or '',
                                 'target': error.target or '',
                                 'error_uri': error.error_uri or '',  # optional TODO:Review error_uri
                                 'date': datetime.now()
                             }
                             )
                            ]
                       })

    # endregion

    def api_auth(self):
        # TODO validate current
        client_id = self.get_config(ConfigKeys.CLIENT_ID.value)
        client_secret = self.get_config(ConfigKeys.CLIENT_SECRET.value)
        basic_params = b64encode(bytes(client_id + ':' + client_secret, "utf-8")).decode("ascii")  # Review Coding
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % basic_params}

        payload = {'grant_type': 'client_credentials', 'scope': 'InvoicingAPI'}  # TODO Read from config
        try:
            response = requests.get("POST", self.api_url_token, headers=headers, data=payload)
            _logger.info(f'{self.api_url_token} called')

            result = response.json()

            if response.status_code == 200:
                # access_token,token_type,expires_in,scope
                self.set_config(ConfigKeys.CLIENT_TOKEN.value, result["access_token"])
                self.set_config(ConfigKeys.CLIENT_TOKEN_TYPE.value, result["token_type"])
                self.set_config(ConfigKeys.CLIENT_TOKEN_EXPIRE_IN.value, str(result["expires_in"]))
                self.set_config(ConfigKeys.SCOPE.value, result["scope"])
                self.set_config(ConfigKeys.CLIENT_TOKEN_LAST_DATE.value, datetime.now().isoformat())
                return result["access_token"]

            else:
                _logger.error(
                    f'Request to get token failed.\nCode:{response.status_code} \nContent: {response.content}')
                self.write_log_all(response)

            return ''
        except Exception as e:
            self._raise_query_error(e)

        # conn = http.client.HTTPSConnection("id.sit.eta.gov.eg")
        #
        # payload = "grant_type=client_credentials&client_id=&client_secret=&scope=InvoicingAPI"
        #
        # headers = {'Content-Type': "application/x-www-form-urlencoded"}
        #
        # conn.request("POST", "/connect/token", payload, headers)
        #
        # res = conn.getresponse()
        # data = res.read()
        #
        # print(data.decode("utf-8"))

        # https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication

        # Content-Type:application/x-www-form-urlencoded
        # from http.client import HTTPSConnection
        # from base64 import b64encode
        # # This sets up the https connection
        # c = HTTPSConnection("www.google.com")
        # # we need to base 64 encode it
        # # and then decode it to acsii as python 3 stores it as a byte string
        # userAndPass = b64encode(b"username:password").decode("ascii")
        # headers = {'Authorization': 'Basic %s' % userAndPass}
        # # then connect
        # c.request('GET', '/', headers=headers)
        # # get the response back
        # res = c.getresponse()
        # # at this point you could check the status etc
        # # this gets the page text
        # data = res.read()

        pass

    # region API Submit Document
    # https://sdk.invoicing.eta.gov.eg/api/05-submit-documents/
    @api.model
    def api_submit_documents(self):
        """
        submit documents
        """
        url = f"{self.get_config(ConfigKeys.API_BASE_URL)}{self.api_url_submit_doc}"
        token = self.validate_token()
        payload = self.get_doc_payload(True)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'ar',
                   'Authorization': f'bearer {token}'}

        try:
            response = requests.get("POST", url, headers=headers, data=payload)
            _logger.info(f'{self.url} called')
            result = response.json()

            if response.status_code == 200:
                responseData = SubmitResponse.from_dict(result)
                for doc in responseData.accepted_documents:
                    self.update_doc_state(doc, responseData.submission_uuid, True)

                for doc in responseData.rejected_documents:
                    self.update_doc_state(doc, '', False)

            else:
                _logger.error(
                    f'Request to get token failed.\nCode:{response.status_code} \nContent: {response.content}')
                self.write_log_all(response)

        except Exception as e:
            self._raise_query_error(e)

    def get_doc_payload(self, validate=False):
        docs_ids = self.env.context.get('active_ids', [])
        if len(self) == 1:
            docs_ids = [self.id]
            # docs_ids.append(self.id)
        docs = DocData()
        docs.documents = list()
        selected_records = self.env['account.move'].browse(docs_ids)

        for invoice in selected_records:
            if validate:  # don't upload document in draft mode
                if invoice.state == 'draft':
                    continue

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

    def update_doc_state(self, doc, submissionUUID, accepted):

        invoice = self.env['account.move'].search([('name', '=', doc.internal_id)], limit=1)
        # doc.internal_id
        if accepted:
            invoice.einv_tax_state = 'valid'
            invoice.einv_post_date = datetime.now()
            invoice.einv_uuid = doc.uuid
            invoice.einv_longId = doc.long_id
            invoice.einv_submissionUUID = submissionUUID
            # TODO:complete other data
            invoice.einv_error_code = ""
            invoice.einv_error_message = ""
            invoice.einv_error_detail = ""

        else:
            invoice.einv_tax_state = 'invalid'
            # invoice.einv_post_date = datetime.now()
            invoice.einv_uuid = doc.uuid
            invoice.einv_longId = doc.long_id
            invoice.einv_submissionUUID = submissionUUID
            # TODO:complete other data
            invoice.einv_error_code = doc.error.code
            invoice.einv_error_message = doc.error.message
            # invoice.einv_error_detail = doc.error.details
            for error in doc.error.details:
                pass

    # return with e-invoice api standard structure -------------------
    def map_doc(self, invoice) -> 'Document':
        doc = Document()
        # invoice
        if invoice.move_type == 'out_invoice':
            doc.document_type = "i"

        elif invoice.move_type == 'out_refund':  # Credit Note#Customer Return
            doc.document_type = "c"
            if invoice.reversed_entry_id and invoice.reversed_entry_id.einv_uuid:
                doc.references.append(invoice.reversed_entry_id.einv_uuid)

        elif invoice.move_type == 'in_refund':  # Debit Note#Vendor Return
            doc.document_type = "d"
            if invoice.reversed_entry_id and invoice.reversed_entry_id.einv_uuid:
                doc.references.append(invoice.reversed_entry_id.einv_uuid)

        doc.document_type_version = self.api_version_number

        # https://www.programiz.com/python-programming/datetime/strftime
        doc.date_time_issued = invoice.invoice_date.strftime('%Y-%m-%dT%H:%M:%SZ') if invoice.invoice_date else ''

        doc.taxpayer_activity_code = self.get_config(ConfigKeys.ACTIVITY_CODE.value) or ''
        doc.internal_id = invoice.name
        doc.purchase_order_reference = ""  # Optional if enable purchase module
        doc.purchase_order_description = ""  # Optional if enable purchase module
        doc.sales_order_reference = ""  # Optional if enable sale module
        doc.sales_order_description = ""  # Optional if enable sale module
        doc.proforma_invoice_number = ""  # Optional: Reference to the previous proforma invoice.

        # Totals
        doc.total_discount_amount = self.compute_total_discount_amount(invoice)  # ToDo: Review total_discount_amount
        # Total amount of discounts: sum of all Discount amount elements of InvoiceLine items.

        doc.total_sales_amount = invoice.amount_untaxed + doc.total_discount_amount  # ToDo: Review total_discount_amount
        # Sum all all InvoiceLine/SalesTotal items

        doc.net_amount = invoice.amount_untaxed
        # TotalSales – TotalDiscount

        doc.extra_discount_amount = 0.0  # ToDo: when add_new
        # Additional discount amount applied at the level of the overall document, not individual lines.

        doc.total_items_discount_amount = doc.extra_discount_amount + doc.total_discount_amount
        # Total amount of item discounts: sum of all Item Discount amount elements of InvoiceLine items.

        doc.total_amount = invoice.amount_total  # ToDo: Review total_amount
        # Total amount of the invoice calculated as NetAmount + Totals of tax amounts. 5 decimal digits allowed.

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
        # partner.address = Address()
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
            # GS1 Egypt https://gs1eg.org/
            # GS1 SA https://www.gs1.org.sa/
            newLine.item_type = line.product_id.einv_coding_schema or self.get_config(
                ConfigKeys.PRODUCT_CODING_SCHEMA.value) or 'GS1'  #
            # Must be GS1 or EGS for this version.

            newLine.item_code = line.product_id.barcode or ""
            # Code of the goods or services item being sold. GS1 codes targeted for managing goods,
            # EGS codes targeted for managing goods – goods or services.

            newLine.unit_type = line.product_uom_id.einv_code or ''  # TODO:Review unit_type .
            newLine.quantity = line.quantity  # Number of units of the defined unit type being sold. Number should be larger than 0.
            newLine.internal_code = line.product_id.default_code or ""
            newLine.sales_total = line.quantity * line.price_unit  # Total amount for the invoice line considering quantity and unit price in EGP
            # (with excluded factory amounts if they are present for specific types in documents).

            newLine.total = line.price_total  # Total amount for the invoice line after
            # adding all pricing items, taxes, removing discounts.

            newLine.value_difference = 0.0
            # Value difference when selling goods already taxed (accepts +/- numbers),
            # e.g., factory value based.

            newLine.total_taxable_fees = 0.0  # Total amount of additional taxable fees to be used in final tax calculation.
            newLine.net_total = line.price_subtotal  # Total amount for the invoice line after applying discount.
            newLine.items_discount = 0.0  # Non-taxable items discount.

            # unit_value: #	The structure defining the price of a single unit sold.
            newLine.unit_value = UnitValue()
            newLine.unit_value.currency_sold = line.currency_id.name
            newLine.unit_value.currency_exchangeRate = 1.0  #
            newLine.unit_value.amount_egp = line.price_unit * newLine.unit_value.currency_exchangeRate
            newLine.unit_value.amount_sold = line.price_unit

            # newLine.discount: # Optional: the structure defining the discount applied on a single unit sold.
            # newLine.discount=Discount()
            newLine.discount.rate = line.discount
            newLine.amount = line.price_unit * line.discount / 100

            # newLine.taxable_items: #Optional: List of taxable items. Can have zero or more of supported tax items
            # below from the list of all tax types including VAT, WHT and table tax, local authority fees (municipality), development.
            newLine.taxable_items = list()
            for tax in line.tax_ids:
                tax_item = TaxableItem()
                tax_item.tax_type = tax.einv_code or 'T12'  # tax.type_tax_use #
                # Type of tax applied - from the list of approved tax type codes.
                # The TaxType needs to be unique across the invoice line (no VAT twice in one invoice line),
                # TaxType is from the list of supported tax types.
                # https: // sdk.invoicing.eta.gov.eg / codes / tax - types /

                tax_item.amount = tax.amount if tax.amount_type == 'fixed' \
                    else line.price_subtotal * tax.amount / 100 if tax.amount_type == 'percent' else 0.0
                # Amount of the tax applied – tax type defined type of tax applies to support different taxes
                # that are possible depending on the type of sales, customer etc. Value with the precision of 2

                tax_item.sub_type = tax.einv_sub_code or ''  #
                # Subtype of the tax type that might mean exemption rate is applied or
                # specific rate linked to product type being sold is applied.

                tax_item.rate = tax.amount if tax.amount_type == 'percent' else 0.0  # Tax rate applied for the invoice line. Value from 0 to 100.

                newLine.taxable_items.append(tax_item)

            lines.append(newLine)

        return lines

    def map_tax_totals(self, invoice_lines):
        # https://sdk.invoicing.eta.gov.eg/codes/tax-types/

        # flatten nested taxes list
        taxes_lines = [item for sublist in ([line.taxable_items for line in invoice_lines])
                       for item in sublist]

        if taxes_lines and len(taxes_lines) > 0:
            taxable_items_dict = TaxesList(taxable_items=taxes_lines).to_dict()
            taxes_groups = sum_group_by(taxable_items_dict["taxableItems"], "taxType", ["amount"])

            tax_totals = [TaxTotal(tax_type=g, amount=taxes_groups[g]['amount']) for g in taxes_groups]
            return tax_totals

        else:
            return list()

        # tax_type
        # Type of tax applied - from the list of approved tax type codes.
        # The TaxType needs to be unique across the invoice line (no VAT twice in one invoice line),
        # TaxType is from the list of supported tax types

        # amount =
        # Sum of all amounts of given tax in all invoice lines. 5 decimal digits allowed.

    def compute_total_discount_amount(self, invoice) -> 'float':

        # self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        # sum(line.price_unit * line.quantity for line in invoice.invoice_line_ids)
        total_before_discount_unit = sum(line.price_unit * line.quantity for line in invoice.invoice_line_ids)
        total_discount_amount = total_before_discount_unit - invoice.amount_untaxed

        return total_discount_amount

    def map_signatures(self):
        # Read from config setting
        signatures = list()

        # 1
        signature = Signature()
        signature.signature_type = self.get_config(ConfigKeys.SIGNATURE_TYPE.value) or "i"
        signature.value = self.get_config(ConfigKeys.SIGNATURE_VALUE.value) or ""
        signatures.append(signature)

        # 2 - if another signature
        return signatures

    # endregion

    # region API Cancel / Reject Document
    # https://sdk.invoicing.eta.gov.eg/api/06-cancel-document/
    def api_cancel_doc(self):
        self.change_doc_status('cancelled', '')  # TODO add confirm form with cancel reason

    # https://sdk.invoicing.eta.gov.eg/api/07-reject-document/
    def api_reject_doc(self):
        self.change_doc_status('rejected', '')  # TODO add confirm form with reject reason

    def change_doc_status(self, state, reason):
        self.ensure_one()
        invoice = self.env['account.move'].search([('id', '=', self.id)], limit=1)
        if invoice.einv_uuid:
            url = f"{self.get_config(ConfigKeys.API_BASE_URL)}/api/v1.0/documents/{invoice.einv_uuid}/state"
            token = self.validate_token()
            payload = {'status': f'{state}', 'reason': f'{reason}'}
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'ar',
                       'Authorization': f'bearer {token}'}

            try:
                response = requests.get("PUT", url, headers=headers, data=payload)
                _logger.info(f'{self.url} called')
                result = response.json()

                if response.status_code == 200:
                    if state == 'cancelled':
                        invoice.einv_tax_state = "cancel_request"  # request succeeded wait for confirm
                        invoice.einv_cancel_request_date = datetime.now()
                    if state == 'rejected':
                        invoice.einv_tax_state = "reject_request"  # request succeeded wait for confirm
                        invoice.einv_reject_request_date = datetime.now()
                else:
                    _logger.error(
                        f'Request to get token failed.\nCode:{response.status_code} \nContent: {response.content}')
                    error = Error.from_dict(result)  # TODO:Review result contains standard error structure
                    self.write_log(invoice, error)
                    # self.write_log_all(response)

            except Exception as e:
                self._raise_query_error(e)

        else:
            # TODO: Raise error that document not submitted
            pass

    # endregion

    # region  Decline Cancellation By (Receiver) | Decline Rejection By(Issuer)

    def decline_request(self, request_name):
        self.ensure_one()
        invoice = self.env['account.move'].search([('id', '=', self.id)], limit=1)
        if invoice.einv_uuid:
            url = f"{self.get_config(ConfigKeys.API_BASE_URL)}/api/v1.0/documents/state/{invoice.einv_uuid}/decline/{request_name}"
            token = self.validate_token()

            headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'ar',
                       'Authorization': f'bearer {token}'}

            try:
                response = requests.get("PUT", url, headers=headers)
                _logger.info(f'{self.url} called')
                result = response.json()

                if response.status_code == 200:
                    invoice.einv_tax_state = "valid"  # change state from '_request' to 'valid'
                    if request_name == 'cancelation':
                        invoice.einv_decline_cancel_request_date = datetime.now()

                    elif request == 'rejection':
                        invoice.einv_decline_reject_request_date = datetime.now()
                else:
                    _logger.error(
                        f'Request to get token failed.\nCode:{response.status_code} \nContent: {response.content}')
                    error = Error.from_dict(result)
                    self.write_log(invoice, error)
                    # self.write_log_all(response)

            except Exception as e:
                self._raise_query_error(e)

        else:
            # TODO: Raise error that document not submitted
            pass

    # https://sdk.invoicing.eta.gov.eg/api/21-decline-cancellation/
    def api_decline_cancellation(self):
        self.decline_request("cancelation")

    # https://sdk.invoicing.eta.gov.eg/api/22-decline-rejection/
    def api_decline_rejection(self):
        self.decline_request("rejection")

    # endregion

    # region  Get recent document
    # https://sdk.invoicing.eta.gov.eg/api/08-get-recent-documents/
    def api_get_recent(self):
        """
        Usage: change document states or check new document received, when found new docs call get detail to add new invoices
        API allows taxpayer systems to query latest documents sent or received that are available on the eInvoicing solution.
        :return: GetRecentResponse
        """

        url = f"{self.get_config(ConfigKeys.API_BASE_URL)}/api/v1.0/documents/recent?"  # ?pageNo={pageNo}&pageSize={pageSize}
        token = self.validate_token()

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'ar',
                   'Authorization': f'bearer {token}'}

        try:
            response = requests.get("GET", url, headers=headers)
            _logger.info(f'{self.url} called')
            result = response.json()
            if response.status_code == 200:
                recent_docs = GetRecentResponse.from_dict(result)
                return recent_docs
            else:
                _logger.error(
                    f'Request to get token failed.\nCode:{response.status_code} \nContent: {response.content}')
                error = Error.from_dict(result)
                # self.write_log(invoice, error)
                # self.write_log_all(response)

        except Exception as e:
            self._raise_query_error(e)

    # endregion

    # region  Get Doc Details
    # https://sdk.invoicing.eta.gov.eg/api/20-get-document-details/
    def api_get_document_details(self, uuid):
        """
        API allows taxpayers to retrieve a single document full details including validation results.
        used when need to add new received  invoice
        :param uuid: Unique e-invoice id number
        :return: GetDocDetailsResponse
        """
        # invoice = self.env['account.move'].search([('einv_uuid', '=', self.uuid)], limit=1)

        url = f"{self.get_config(ConfigKeys.API_BASE_URL)}/api/v1.0/documents/{uuid}/details"
        token = self.validate_token()

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'ar',
                   'Authorization': f'bearer {token}'}

        try:
            response = requests.get("PUT", url, headers=headers)
            _logger.info(f'{self.url} called')
            result = response.json()

            if response.status_code == 200:
                doc = GetDocDetailsResponse.from_dict(result)
                return doc
            else:
                _logger.error(
                    f'Request to get token failed.\nCode:{response.status_code} \nContent: {response.content}')

        except Exception as e:
            self._raise_query_error(e)

    # endregion

    # region  Get Document
    # https://sdk.invoicing.eta.gov.eg/api/12-get-document/
    def api_get_document(self, uuid):
        """
        API allows taxpayers to retrieve document source XML or JSON with additional tax authority added metadata.
         used when need to add new received  invoice
        :param uuid: Unique e-invoice id number
        :return: GetDocResponse
        """

        url = f"{self.get_config(ConfigKeys.API_BASE_URL)}/api/v1.0/documents/{uuid}/raw"
        token = self.validate_token()

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'ar',
                   'Authorization': f'bearer {token}'}

        try:
            response = requests.get("PUT", url, headers=headers)
            _logger.info(f'{self.url} called')
            result = response.json()

            if response.status_code == 200:
                doc = GetDocResponse.from_dict(result)
                return doc
            else:
                _logger.error(
                    f'Request to get token failed.\nCode:{response.status_code} \nContent: {response.content}')



        except Exception as e:
            self._raise_query_error(e)

    # endregion

    # region  Receive New Invoice or update status
    def fetch_recent_docs(self):
        recent_docs = self.api_get_recent()
        if recent_docs and recent_docs.result:
            for doc in recent_docs.result:
                invoice = self.env['account.move'].search([('name', '=', doc.internal_id)], limit=1)
                if invoice:
                    self.sync_doc_state(invoice, doc)
                else:
                    self.create_invoice(doc)

    def sync_doc_state(self, invoice, doc):
        if invoice.einv_tax_state != doc.status:
            invoice.einv_issued_date = from_datetime(doc.date_time_issued)
            invoice.einv_received_date = from_datetime(doc.date_time_received)
            invoice.einv_cancel_request_date = from_datetime(doc.cancel_request_date)
            invoice.einv_reject_request_date = from_datetime(doc.reject_request_date)
            invoice.einv_cancel_request_delayed_date = from_datetime(doc.cancel_request_delayed_date)
            invoice.einv_reject_request_delayed_date = from_datetime(doc.reject_request_delayed_date)
            invoice.einv_decline_cancel_request_date = from_datetime(doc.decline_cancel_request_date)
            invoice.einv_decline_reject_request_date = from_datetime(doc.decline_reject_request_date)

            invoice.einv_tax_state = doc.status
            # self.env.cr.commit()

    def create_invoice(self, document):
        doc = self.api_get_document(document.uuid)
        if doc:
            partner = doc.document.issuer if doc.receiver_id == self.env.company.vat else doc.document.receiver
            invoice = {
                'move_type': self.get_move_type(doc),
                'name': doc.internal_id,
                'partner_id': self.create_partner(partner).id
                #TODO complete invoice creation

            }
            self.env['account.move'].create(invoice)

    def get_move_type(self, doc):
        """
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        :param doc:
        :return: str
        """
        if doc.receiver_id == self.env.company.vat:  # document is in_invoice
            if doc.type_name.lower() == "c":  # credit note
                return "in_refund"
            elif doc.type_name.lower() == "d":  # credit note
                return "in_invoice"  # TODO: change to debitnote
            else:
                return "in_invoice"  # default
        else:  # "out_invoice"
            if doc.type_name.lower() == "c":  # credit note
                return "out_refund"
            elif doc.type_name.lower() == "d":  # credit note
                return "out_invoice"  # TODO: change to debitnote
            else:
                return "out_invoice"

    def get_partner(self, register_number):
        return self.env['res.partner'].search([('vat', '=', register_number)], limit=1)

    def get_country(self, code):
        return self.env['res.country'].search([('code', '=', code)], limit=1)

    def get_state(self, name):
        return self.env['res.country.state'].search([('name', '=', name)], limit=1)


    def create_partner(self, partner):
        """
        get or create partner if not exist
        :param partner: 
        :return: 
        """
        res_partner = self.get_partner(self, partner.id)
        if partner:
            return res_partner
        else:
            # partner type    # B for business in Egypt, P for natural person, F for
            country = self.get_country(partner.address.country)
            state = self.get_country(partner.address.governate)
            new_res_partner = {
                'is_company': True if partner.type.upper() == "B" else False,
                'is_person': True if partner.type.upper() == "P" else False,
                'name': partner.name,
                'vat': partner.id,
                'country_id': country.id if country else None,
                'state_id': state.id if state else None,
                'city': partner.address.region_city,
                'street': partner.address.street,
                'street2': partner.address.building_number,
                'zip': partner.address.postal_code
            }
            self.env['res.partner'].create(new_res_partner)

    # endregion

    # region  Decline Rejection (Issuer)

    # endregion

    # region Automation Scheduled Task
    # https://www.youtube.com/watch?v=_P_AVSNr6uU
    # https://odoo-development.readthedocs.io/en/latest/odoo/models/ir.cron.html#:~:text=Schedulers%20are%20automated%20actions%20that,will%20execute%20it%20as%20defined.
    # endregion


class EgtaxApiController(http.Controller):

    @http.route('/web/einv/api/doc/download/<string:res_model>/<int:res_id>', type='http', auth="public")
    # @serialize_exception
    def download_doc(self, res_model, res_id, ):
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
