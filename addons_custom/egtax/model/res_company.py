#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ResCompany(models.Model):

    _name = "res.company"
    _description = "res.company"
    _inherit = "res.company"

    einv_activity_id = fields.Many2one('egtax.activity_type', string="Activity Type", required=True)




