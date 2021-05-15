#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class UnitType(models.Model):

    _name = "egtax.unit_type"
    _description = "egtax.unit_type"
    _inherit = "egtax.base_code"


