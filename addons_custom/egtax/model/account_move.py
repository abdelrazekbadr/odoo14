#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _, http
from odoo.exceptions import UserError, Warning, ValidationError
from odoo.http import serialize_exception, request
from datetime import datetime


class AccountMove(models.Model):
    _name = "account.move"
    _description = "account.move"

    _inherit = ["account.move", "egtax.einv_api"]
    # “submitted”, “valid”, “invalid”, “rejected”, “cancelled”
    einv_tax_state = fields.Selection(selection=[
        ('draft', 'Ready'),
        ('submitted', 'Submitted'),
        ('valid', 'Sent'),
        ('invalid', 'Error'),
        ('reject_request', 'Reject Request'),
        ('rejected', 'Rejected'),
        ('cancel_request', 'Cancel Request'),
        ('cancelled', 'Cancelled')], string="Tax Status", help="", default="draft")

    einv_tax_state_display = fields.Selection(selection=[
        ('draft', 'Ready'),
        ('submitted', 'Submitted'),
        ('valid', 'Sent'),
        ('invalid', 'Error'),
        ('reject_request', 'Reject Request'),
        ('rejected', 'Rejected'),
        ('cancel_request', 'Cancel Request'),
        ('cancelled', 'Cancelled')], compute='_compute_einv_tax_state_display',
        string="Tax Status", help="", default="draft")
    partner_display_name = fields.Char(string="Customer/Vendor", compute="_compute_partner_display_name")

    einv_post_date = fields.Datetime(string="Sent Date", help="")
    einv_is_submitted = fields.Boolean(string="Submitted", help="")
    einv_uuid = fields.Char(string="UUID", help="")
    einv_longId = fields.Char(string="Long ID", help="")
    einv_submissionUUID = fields.Char(string="Submission UUID", help="")
    einv_error_code = fields.Char(string="Error Code", help="")
    einv_error_message = fields.Char(string="Error Message", help="")
    einv_error_target = fields.Char(string="Error Target", help="")
    einv_error_detail = fields.Text(string="Error Detail", help="")
    einv_doc_json = fields.Text(string="JSON Data", compute="_compute_preview_json")
    einv_doc_json_Test = fields.Text(string="JSON Test")

    einv_action_type = fields.Selection(selection=[
        ('auto', 'Auto'),
        ('manual', 'Manual')],
        string="Action Type", help="", default="manual")

    einv_issued_date = fields.Datetime(string="Issue Date", help="")
    einv_received_date = fields.Datetime(string="Received Date", help="")
    einv_cancel_request_date = fields.Datetime(string="Cancel Request Date", help="")
    einv_reject_request_date = fields.Datetime(string="Reject Request Date", help="")
    einv_cancel_request_delayed_date = fields.Datetime(string="Request Delayed Date", help="")
    einv_reject_request_delayed_date = fields.Datetime(string="Reject Request Delayed Date", help="")
    einv_decline_cancel_request_date = fields.Datetime(string="Decline Cancel Request Date", help="")
    einv_decline_reject_request_date = fields.Datetime(string="Decline Reject  Request Date", help="")

    errors_detail_ids = fields.One2many(comodel_name="egtax.error", inverse_name="invoice_id", string="Errors Detail",
                                        help="")

    @api.depends('einv_tax_state')
    def _compute_einv_tax_state_display(self):
        for r in self:
            r.einv_tax_state_display = r.einv_tax_state or 'draft'
            if not r.einv_tax_state:
                r.einv_tax_state = 'draft'

    @api.depends('partner_id')
    def _compute_partner_display_name(self):
        for r in self:
            r.partner_display_name = r.partner_id.name

    # preview in formview only
    def _compute_preview_json(self):
        self.ensure_one()
        docs_ids=[self.id]
        self.einv_doc_json = json.dumps(self.get_doc_payload(docs_ids), indent=4, sort_keys=True)

    # def create_invoice_from_json(self):
    #    #jsonData= json.loads(self.einv_doc_json_Test)
    #    self.test_add_invoice_from_json()
    #     # if self is AccountMove:
    #     #     self.einv_doc_json =json.dumps(self.get_doc_payload())
    #
    #     # for record in self:
    #     #     record.einv_doc_json = ''

    def preview_doc_json(self):
        for record in self:
            record.einv_doc_json = ''
