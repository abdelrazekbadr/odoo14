#!/usr/bin/python
# -*- coding: utf-8 -*-
# help:https://www.cybrosys.com/blog/odoo-13-technical-tips-tricks
from odoo import models, fields, api, _
from odoo.addons.egtax.enums.config_keys import ConfigKeys
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
    last_token_date = fields.Datetime(string="Last token date", readonly=True, help="")
    signature_type = fields.Selection(selection=[('i', 'Issuer '), ('s', 'Service Provider')], string="Signature type",
                                      help="")
    signature_value = fields.Text(string="Signature value", help="")

    activity_id = fields.Many2one('egtax.activity_type', string="Activity Type", required=True)
    activity_code = fields.Char(string="Activity Code", help="")

    token_type = fields.Char(string="Token Type", readonly=True, help="")
    expire_in = fields.Char(string="Expire_in", readonly=True, help="")
    #key_client_token_type = 'egtax.token_type'
    #key_expire_in = 'egtax.token_expire_in'

    #default_coding_schema = fields.Char(string="Defult Coding", help="", default="GS1")
    # Usage => param = self.env['ir.config_parameter'].sudo().get_param(ConfigKeys.apiBaseUrl') or False
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config = self.env['ir.config_parameter'].sudo()

        res.update(
            scope=config.get_param(ConfigKeys.SCOPE) or "InvoicingAPI",#config.get_param(ConfigKeys.activity_id'),
            grant_type=config.get_param(ConfigKeys.GRANT_TYPE.value) or "client_credentials",
            client_id=config.get_param(ConfigKeys.CLIENT_ID.value),
            client_secret=config.get_param(ConfigKeys.CLIENT_SECRET.value),
            apiBaseUrl=config.get_param(ConfigKeys.API_BASE_URL.value) or "https://api.sit.invoicing.eta.gov.eg",
            idSrvBaseUrl=config.get_param(ConfigKeys.ID_SRV_BASE_URL.value) or "https://id.sit.eta.gov.eg",
            client_token=config.get_param(ConfigKeys.CLIENT_TOKEN.value),
            auto_post=bool(config.get_param(ConfigKeys.AUTO_POST.value)) ,
            last_token_date=config.get_param(ConfigKeys.CLIENT_TOKEN_LAST_DATE.value),
            signature_type=config.get_param(ConfigKeys.SIGNATURE_TYPE.value),
            signature_value=config.get_param(ConfigKeys.SIGNATURE_VALUE.value),
            activity_id= int(config.get_param(ConfigKeys.ACTIVITY_ID.value)),
            activity_code = config.get_param(ConfigKeys.ACTIVITY_CODE.value),
            product_coding_schema =config.get_param(ConfigKeys.PRODUCT_CODING_SCHEMA.value) or 'GS1',
            token_type=config.get_param(ConfigKeys.CLIENT_TOKEN_TYPE.value) or '',
            expire_in=config.get_param(ConfigKeys.CLIENT_TOKEN_EXPIRE_IN.value) or ''
            #default_coding_schema = config.get_param(ConfigKeys.default_coding_schema') or 'GS1'
        )

        return res

    @api.model
    def set_values(self):
        config = self.env['ir.config_parameter'].sudo()
        config.set_param(ConfigKeys.SCOPE.value, self.scope)
        config.set_param(ConfigKeys.GRANT_TYPE.value, self.grant_type)
        config.set_param(ConfigKeys.CLIENT_ID.value, self.client_id)
        config.set_param(ConfigKeys.client_secret.value, self.client_secret)
        config.set_param(ConfigKeys.API_BASE_URL.value, self.apiBaseUrl)
        config.set_param(ConfigKeys.ID_SRV_BASE_URL.value, self.idSrvBaseUrl)
        config.set_param(ConfigKeys.CLIENT_TOKEN.value, self.client_token)
        config.set_param(ConfigKeys.AUTO_POST.value, self.auto_post)
        config.set_param(ConfigKeys.CLIENT_TOKEN_LAST_DATE.value, self.last_token_date)
        config.set_param(ConfigKeys.SIGNATURE_TYPE.value, self.signature_type)
        config.set_param(ConfigKeys.SIGNATURE_VALUE.value, self.signature_value)

        config.set_param(ConfigKeys.ACTIVITY_ID.value, self.activity_id.id)
        config.set_param(ConfigKeys.ACTIVITY_CODE.value, self.activity_id.code)

        config.set_param(ConfigKeys.PRODUCT_CODING_SCHEMA.value, self.product_coding_schema)

        #config.set_param(ConfigKeys.default_coding_schema.value, self.default_coding_schema)

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
