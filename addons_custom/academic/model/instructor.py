#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class instructor(models.Model):

    _name = "res.partner"
    _description = "res.partner"

    _inherit = "res.partner"
    is_instructor = fields.Boolean( string="Is instructor",  help="")


    session_ids = fields.One2many(comodel_name="academy.session",  inverse_name="instructor_id",  string="Sessions",  help="")
