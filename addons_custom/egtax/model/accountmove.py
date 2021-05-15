#!/usr/bin/python
#-*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _,http
from odoo.exceptions import UserError, Warning, ValidationError
from odoo.http import serialize_exception, request


class AccountMove(models.Model):

    _name = "account.move"
    _description = "account.move"

    _inherit = ["account.move","egtax.einv_api"]
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
    partner_display_name = fields.Char(string="Customer/Vendor",compute="_compute_partner_display_name")

    einv_post_date = fields.Date( string="Tax Post Date",  help="")
    einv_uuid = fields.Char( string="UUID",  help="")
    einv_longId = fields.Char( string="Long ID",  help="")
    einv_submissionUUID = fields.Char( string="Submission UUID",  help="")
    einv_error_code = fields.Char( string="Error Code",  help="")
    einv_error_message = fields.Char( string="Error Message",  help="")
    einv_error_target = fields.Char( string="Error Target",  help="")
    einv_error_detail = fields.Text( string="Error Detail",  help="")
    einv_doc_json = fields.Text(string="JSON Data", compute="_compute_preview_json")


    errors_detail = fields.One2many(comodel_name="egtax.error",  inverse_name="invoice_id",  string="Errors Detail",  help="")

    @api.depends('einv_tax_state')
    def _compute_einv_tax_state_display(self):
        for r in self:
            r.einv_tax_state_display = r.einv_tax_state or 'draft'

    @api.depends('partner_id')
    def _compute_partner_display_name(self):
        for r in self:
            r.partner_display_name = r.partner_id.name


    def action_post_tax(self):
        # define e-invoice api to send post
        #self.einv_tax_state=''
        # config = self.env['ir.config_parameter'].sudo()
        # client_id = config.get_param('egtax.client_id')
        # client_secret = config.get_param('egtax.client_secret')
        # apiBaseUrl = config.get_param('egtax.apiBaseUrl')
        # idSrvBaseUrl = config.get_param('egtax.idSrvBaseUrl')
        # auto_post = bool(config.get_param('egtax.auto_post'))

        #selected_ids=self.env.context.get('active_ids', [])
        self.api_submit_documents()

        raise ValidationError(_("This action isn't available for this document."))
        # for r in self:
        #     r.partner_display_name = r.partner_id.name

    def action_register_payment2(self):
        ''' Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        '''
        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    #preview in formview only
    def _compute_preview_json(self):
        self.einv_doc_json = json.dumps(self.get_doc_payload(), indent=4, sort_keys=True)
        # if self is AccountMove:
        #     self.einv_doc_json =json.dumps(self.get_doc_payload())

        # for record in self:
        #     record.einv_doc_json = ''

    def preview_doc_json(self):
        for record in self:
            record.einv_doc_json = ''
