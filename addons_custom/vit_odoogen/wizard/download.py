from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class DownloadConfirm(models.TransientModel):
    _name = 'vit.download_wizard'
    _description = 'Download Confirmation'

    def confirm_button(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}
