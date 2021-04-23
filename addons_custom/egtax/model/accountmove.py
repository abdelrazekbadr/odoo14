#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class AccountMove(models.Model):

    _name = "account.move"
    _description = "account.move"

    _inherit = "account.move"
    einv_tax_state = fields.Selection(selection=[
        ('draft','Draft'),
        ('post','Post'),
        ('cancel','Cancel'),
        ('reject','Reject')],string="Tax Status",  help="",defult="draft")

    einv_tax_state_display = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('post', 'Post'),
        ('cancel', 'Cancel'),
        ('reject', 'Reject')],compute='_compute_einv_tax_state_display',
        string="Tax Status", help="",defult="draft")


    einv_post_date = fields.Date( string="Tax Post Date",  help="")
    einv_uuid = fields.Char( string="UUID",  help="")
    einv_longId = fields.Char( string="Long ID",  help="")
    einv_submissionUUID = fields.Char( string="Submission UUID",  help="")
    einv_error_code = fields.Char( string="Error Code",  help="")
    einv_error_message = fields.Char( string="Error Message",  help="")
    einv_error_target = fields.Char( string="Error Target",  help="")
    einv_error_detail = fields.Text( string="Error Detail",  help="")


    errors_detail = fields.One2many(comodel_name="egtax.error",  inverse_name="invoice_id",  string="Errors Detail",  help="")

    @api.depends('einv_tax_state')
    def _compute_einv_tax_state_display(self):
        for r in self:
            r.einv_tax_state_display = r.einv_tax_state or 'draft'