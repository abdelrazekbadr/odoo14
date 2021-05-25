#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


class Error(models.Model):
    _name = "egtax.error"
    _description = "egtax.error"

    code = fields.Char(string="Code", help="")
    name = fields.Char(string="Name", help="")
    message = fields.Char(string="Message", help="")
    target = fields.Char(string="Target", help="")
    date = fields.Datetime(string="Date", help="")
    error_uri = fields.Char(string="URI", help="")

    invoice_id = fields.Many2one(comodel_name="account.move", string="Invoice", help="",invisible="1")
