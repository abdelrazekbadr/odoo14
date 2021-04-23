#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class session(models.Model):
    """session yang ada dalam suatu course, memiliki 1 instruktor berupa res.partner"""

    _name = "academy.session"
    _description = "academy.session"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")
    date_start = fields.Date( string="Date start",  help="")
    duration = fields.Integer( string="Duration",  help="")
    seats = fields.Integer( string="Seats",  help="")


    #course_id = fields.Many2one(comodel_name="academy.course",  string="Course",  help="")
    #instructor_id = fields.Many2one(comodel_name="academy.instructor",  string="Instructor",  help="")
    #attendee_ids = fields.One2many(comodel_name="academy.attendee",  inverse_name="session_id",  string="Attendees",  help="")
