# -*- coding: utf-8 -*-
# from odoo import http


# class CdnRentalArmada(http.Controller):
#     @http.route('/cdn_rental_armada/cdn_rental_armada', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cdn_rental_armada/cdn_rental_armada/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cdn_rental_armada.listing', {
#             'root': '/cdn_rental_armada/cdn_rental_armada',
#             'objects': http.request.env['cdn_rental_armada.cdn_rental_armada'].search([]),
#         })

#     @http.route('/cdn_rental_armada/cdn_rental_armada/objects/<model("cdn_rental_armada.cdn_rental_armada"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cdn_rental_armada.object', {
#             'object': obj
#         })
