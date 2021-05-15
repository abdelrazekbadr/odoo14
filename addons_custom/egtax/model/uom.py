#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class UoM(models.Model):

    _name = "uom.uom"
    _description = "uom.uom"
    _inherit = "uom.uom"

    einv_code = fields.Char( string="Code",  help="")
    einv_module = fields.Char(string="Module", help="",default="egtax")

class UoMCategory(models.Model):
    _name = 'uom.category'
    _inherit = 'uom.category'

    einv_module = fields.Char(string="Module", help="",default="egtax")


