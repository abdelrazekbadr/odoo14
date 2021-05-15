#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ActivityType(models.Model):

    _name = "egtax.activity_type"
    _description = "egtax.activity_type"
    _inherit = "egtax.base_code"


