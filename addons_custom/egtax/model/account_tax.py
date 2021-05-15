#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class AccountTax(models.Model):

    _name = "account.tax"
    _description = "account.tax"

    _inherit = "account.tax"


    einv_code = fields.Char( string="eInv Code",  help="",compute="_compute_code" ,store="True")
    einv_sub_code = fields.Char(string="eInv Sub Code",  help="",compute="_compute_code" ,store="True")


    einv_tax_type_id = fields.Many2one(comodel_name="egtax.tax_type", string="Category", help="")

    @api.depends('einv_tax_type_id')
    def _compute_code(self):
        for r in self:
            if r.einv_tax_type_id and r.einv_tax_type_id.parent_id: #subtypes
                r.einv_sub_code = r.einv_tax_type_id.code or ''
                r.einv_code = r.einv_tax_type_id.parent_id.code or ''
            elif r.einv_tax_type_id and not r.einv_tax_type_id.parent_id: # parent
                r.einv_code = r.einv_tax_type_id.code or ''