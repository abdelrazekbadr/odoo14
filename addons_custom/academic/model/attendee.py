#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class attendee(models.Model):

    _name = "academy.attendee"
    _description = "academy.attendee"
    name = fields.Char( required=True, string="Name",  help="")


    session_id = fields.Many2one(comodel_name="academy.session",  string="Session",  help="")
    partner_id = fields.Many2one(comodel_name="res.partner",  string="Partner",  help="")
