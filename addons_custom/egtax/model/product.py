from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class Product(models.Model):

    _name = "product.template"
    _description = "product.template"
    _inherit = "product.template"


    einv_coding_schema = fields.Selection(selection=[
        ('gs1', 'GS1'),('egs', 'EGS')
       ],
        string="Coding Schema", help="", default='gs1')
