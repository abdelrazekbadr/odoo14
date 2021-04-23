#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class course(models.Model):
    """
    course master data, bisa punya banyak session.
    memiliki 1 penaggung jawab
    """

    _name = "academy.course"
    _description = "academy.course"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")


    session_ids = fields.One2many(comodel_name="academy.session",  inverse_name="course_id",  string="Sessions",  help="")
    responsible_id = fields.Many2one(comodel_name="res.users",  string="Responsible",  help="")
