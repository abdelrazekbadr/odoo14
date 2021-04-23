#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class user(models.Model):

    _name = "res.users"
    _description = "res.users"

    _inherit = "res.users"


    course_ids = fields.One2many(comodel_name="academy.course",  inverse_name="responsible_id",  string="Courses",  help="")
