#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class TaxType(models.Model):

    _name = "egtax.tax_type"
    _description = "egtax.tax_type"
    _inherit = "egtax.base_code"

    is_non_taxable = fields.Boolean(string="Non taxable", help="")

    parent_id = fields.Many2one(comodel_name="egtax.tax_type", string="Parent", help="")
    children_ids = fields.One2many(comodel_name="egtax.tax_type", inverse_name="parent_id", string="Sub Types", help="")
    tax_ids = fields.One2many(comodel_name="account.tax", inverse_name="einv_tax_type_id", string="Taxes", help="")


