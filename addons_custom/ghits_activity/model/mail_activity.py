#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class MailActivity(models.Model):
    _inherit = "mail.activity"

    def action_open_form(self):
        self.ensure_one()
        # context = dict(self.env.context)
        # context['form_view_initial_mode'] = 'edit'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Activities',
            'target': 'current',  #'new' use 'current' for not opening in a dialog
            'res_model':self.res_model, #'target.model',
            'res_id': self.res_id,# target_id,
             #'view_id': 'view_xml_id',  # optional
            'view_type': 'form',
            'view_mode':'form',
            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'},
            'flags': {'initial_mode': 'edit'}
        };






