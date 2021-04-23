#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class Error(models.Model):

    _name = "egtax.error"
    _description = "egtax.error"

    code = fields.Char( string="Code",  help="")
    message = fields.Char( string="Message",  help="")
    target = fields.Char( string="Target",  help="")
    date = fields.Date( string="Date",  help="")


    invoice_id = fields.Many2one(comodel_name="account.move",  string="Invoice",  help="")
