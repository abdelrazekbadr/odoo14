#!/usr/bin/python
# -*- coding: utf-8 -*-
# help:https://www.cybrosys.com/blog/odoo-13-technical-tips-tricks
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    # _name = "egtax.setting"
    # _description = "egtax.setting"

    scope = fields.Char(string="Scope", help="",default="InvoicingAPI")
    grant_type = fields.Char(string="Grant Type", help="",default="client_credentials")
    client_id = fields.Char(string="Client ID", help="")
    client_secret = fields.Char(string="Client Secret", help="")
    apiBaseUrl = fields.Char(string="API  URL", help="",default="https://api.sit.invoicing.eta.gov.eg")
    idSrvBaseUrl = fields.Char(string="Server URL", help="",default="https://id.sit.eta.gov.eg")
    product_coding_schema = fields.Char(string="Coding Schema", help="", default="GS1")
    client_token = fields.Char(string="Client Token", readonly=False, help="")
    auto_post = fields.Boolean(string="Auto Post", help="")
    last_token_date = fields.Date(string="Last token date", readonly=False, help="")
    signature_type = fields.Selection(selection=[('i', 'Issuer '), ('s', 'Service Provider')], string="Signature type",
                                      help="")
    signature_value = fields.Text(string="Signature value", help="")

    activity_id = fields.Many2one('egtax.activity_type', string="Activity Type", required=True)
    activity_code = fields.Char(string="Activity Code", help="")
    #default_coding_schema = fields.Char(string="Defult Coding", help="", default="GS1")
    # Usage => param = self.env['ir.config_parameter'].sudo().get_param('egtax.apiBaseUrl') or False
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config = self.env['ir.config_parameter'].sudo()

        res.update(
            scope=config.get_param('egtax.scope') or "InvoicingAPI",#config.get_param('egtax.activity_id'),
            grant_type=config.get_param('egtax.grant_type') or "client_credentials",
            client_id=config.get_param('egtax.client_id'),
            client_secret=config.get_param('egtax.client_secret'),
            apiBaseUrl=config.get_param('egtax.apiBaseUrl') or "https://api.sit.invoicing.eta.gov.eg",
            idSrvBaseUrl=config.get_param('egtax.idSrvBaseUrl') or "https://id.sit.eta.gov.eg",
            client_token=config.get_param('egtax.client_token'),
            auto_post=bool(config.get_param('egtax.auto_post')) ,
            last_token_date=config.get_param('egtax.last_token_date'),
            signature_type=config.get_param('egtax.signature_type'),
            signature_value=config.get_param('egtax.signature_value'),
            activity_id= int(config.get_param('egtax.activity_id')),
            activity_code = config.get_param('egtax.activity_code'),
            product_coding_schema = config.get_param('egtax.product_coding_schema') or 'GS1'
            #default_coding_schema = config.get_param('egtax.default_coding_schema') or 'GS1'
        )

        return res

    @api.model
    def set_values(self):
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('egtax.scope', self.scope)
        config.set_param('egtax.grant_type', self.grant_type)
        config.set_param('egtax.client_id', self.client_id)
        config.set_param('egtax.client_secret', self.client_secret)
        config.set_param('egtax.apiBaseUrl', self.apiBaseUrl)
        config.set_param('egtax.idSrvBaseUrl', self.idSrvBaseUrl)
        config.set_param('egtax.client_token', self.client_token)
        config.set_param('egtax.auto_post', self.auto_post)
        config.set_param('egtax.last_token_date', self.last_token_date)
        config.set_param('egtax.signature_type', self.signature_type)
        config.set_param('egtax.signature_value', self.signature_value)

        config.set_param('egtax.activity_id', self.activity_id.id)
        config.set_param('egtax.activity_code', self.activity_id.code)

        config.set_param('egtax.product_coding_schema',self.product_coding_schema)

        #config.set_param('egtax.default_coding_schema', self.default_coding_schema)

        super(ResConfigSettings, self).set_values()

    # @api.model
    # def get_values(self):
    #     res = super(Setting, self).get_values()
    #     alias = self._find_default_lead_alias_id()
    #     res.update(
    #         crm_alias_prefix=alias.alias_name if alias else False,
    #     )
    #     return res
    #
    # def set_values(self):
    #     super(Setting, self).set_values()
    #     alias = self._find_default_lead_alias_id()
    #     if alias:
    #         alias.write({'alias_name': self.crm_alias_prefix})
    #     else:
    #         self.env['mail.alias'].create({
    #             'alias_name': self.crm_alias_prefix,
    #             'alias_model_id': self.env['ir.model']._get('crm.lead').id,
    #             'alias_parent_model_id': self.env['ir.model']._get('crm.team').id,
    #         })
    #     for team in self.env['crm.team'].search([]):
    #         team.alias_id.write(team._alias_get_creation_values())
