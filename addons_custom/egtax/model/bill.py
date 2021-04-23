#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class Bill(models.Model):

    _name = "account.move"
    _description = "account.move"

    _inherit = "account.move"


