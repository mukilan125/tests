# -*- coding: utf-8 -*-
from odoo import http

# class MasterCustom(http.Controller):
#     @http.route('/master_custom/master_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/master_custom/master_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('master_custom.listing', {
#             'root': '/master_custom/master_custom',
#             'objects': http.request.env['master_custom.master_custom'].search([]),
#         })

#     @http.route('/master_custom/master_custom/objects/<model("master_custom.master_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('master_custom.object', {
#             'object': obj
#         })