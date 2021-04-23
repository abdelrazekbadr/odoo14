# -*- coding: utf-8 -*-

from odoo import models, fields, api

#non persistent object
class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_session(self):
        # return self.env['openacademy.session'].browse(self._context.get('active_id')) #single item
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))  # multiple item

    # session_id = fields.Many2one('openacademy.session',
    #     string="Session", required=True, default=_default_session)

    session_ids = fields.Many2many('openacademy.session',
                                     string="Sessions", required=True, default=_default_session)

    attendee_ids = fields.Many2many('res.partner', string="Attendees")


    def subscribe(self):
        self.session_id.attendee_ids |= self.attendee_ids
        # |= [exclusive or] to add different list items
        return {}