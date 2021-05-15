#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class BaseCode(models.Model):

    _name = "egtax.base_code"
    _description = "egtax.base_code"
    name = fields.Char(string="Name",  help="",compute='_compute_name',search="_search_field")
    code = fields.Char( string="Code",  help="")
    desc_ar = fields.Char( string="Arabic Description",  help="")
    desc_en = fields.Char( string="English Description",  help="")

    @api.depends('desc_en','desc_ar')
    #@api.multi
    def _compute_name(self):
        lang=self.env.lang
        for r in self:
            if lang.startswith("ar"):
                if r.desc_ar and r.desc_ar != "":
                    r.name = r.desc_ar
                else:
                    r.name = r.desc_en
            else:
               r.name = r.desc_en

    def _search_field(self, operator, value):
        records = self.search([]).filtered(lambda x: value in x.desc_ar or value in x.desc_en)
        return [('id', 'in', records.ids)]
        #return [('id', operator, [x.id for x in field_ids] if field_ids else False)]


