#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class partner(models.Model):

    _name = "res.partner"
    _description = "res.partner"

    _inherit = "res.partner"


    attendee_ids = fields.One2many(comodel_name="academy.attendee",  inverse_name="partner_id",  string="Attendees",  help="")
