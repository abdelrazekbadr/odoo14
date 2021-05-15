
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import requests
import logging
#import pydantic
from odoo import api, fields, models, tools, _
from ..api.documents import *


from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

class EInvAPI(models.AbstractModel):
    _name = "egtax.einv_api"
    _description = "Eg E-Invoice API "

    api_version="v1"
    api_token="/connect/token"
    api_documentsubmissions=f"/api/{api_version}/documentsubmissions"

    client_id =""
    client_secret = ""
    apiBaseUrl = ""
    idSrvBaseUrl = ""
    auto_post = False
    token =""
    def __init__(self):
        config = self.env['ir.config_parameter'].sudo()
        self.client_id = config.get_param('egtax.client_id')
        self.client_secret = config.get_param('egtax.client_secret')
        self.apiBaseUrl = config.get_param('egtax.apiBaseUrl')
        self.idSrvBaseUrl = config.get_param('egtax.idSrvBaseUrl')
        self.auto_post = bool(config.get_param('egtax.auto_post'))
    #

    #def submit_documents(self):
    @api.model
    def submit_documents(self, docs_ids):
        """
        submit documents
        """
        if not docs_ids:
            _logger.info('invalid address given')
            return None
        #selected_ids = self.env.context.get('active_ids', [])
        docs = DocData()
        selected_records = self.env['account.move'].browse(docs_ids)
        for r in selected_records:
            doc = Document()
            #fill data from invoice document


            docs.documents.insert(doc)




        url = f"{self.apiBaseUrl}{self.api_documentsubmissions}"
        payload=docs.to_dict()

        # try:
        #     headers = {'Content-Type': 'application/json','Authorization':f'bearer {self.token}'}
        #     #params = {'format': 'json', 'q': addr}
        #     response = requests.get("POST",url, headers=headers,data=payload)
        #     _logger.info(f'{url} called')
        #     if response.status_code != 200:
        #         _logger.error('Request to openstreetmap failed.\nCode: %s\nContent: %s' % (response.status_code, response.content))
        #     result = response.json()
        # except Exception as e:
        #     self._raise_query_error(e)
        #





