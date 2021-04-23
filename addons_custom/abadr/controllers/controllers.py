# -*- coding: utf-8 -*-
# from odoo import http


# class Abadr(http.Controller):
#     @http.route('/abadr/abadr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/abadr/abadr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('abadr.listing', {
#             'root': '/abadr/abadr',
#             'objects': http.request.env['abadr.abadr'].search([]),
#         })

#     @http.route('/abadr/abadr/objects/<model("abadr.abadr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('abadr.object', {
#             'object': obj
#         })
