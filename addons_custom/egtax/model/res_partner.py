#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ResPartner(models.Model):

    _name = "res.partner"
    _description = "res.partner"
    _inherit = "res.partner"

    einv_activity_id = fields.Many2one('egtax.activity_type', string="Activity Type")




