import base64
from odoo import http
from odoo.http import request

class ArmadaSite(http.Controller):
    @http.route('/armada', auth='public', website=True)
    def index(self, **kw):
        armadas = request.env['cdn.armada'].sudo().search([('priority', '=', 1)])
        return request.render('cdn_rental_armada.armada_list', {'armadas': armadas})
    
    @http.route('/' , auth='public', website=True)
    def home(self, **kw):
        products = request.env['cdn.produk.armada'].sudo().search([])
        return request.render('cdn_rental_armada.product_list', {'products': products})
    