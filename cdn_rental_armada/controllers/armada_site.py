import base64
from odoo import http
from odoo.http import request

class ArmadaSite(http.Controller):
    @http.route('/' , auth='public', website=True)
    def home(self, **kw):
        products = request.env['cdn.produk.armada'].sudo().search([('priority', '=', '1')])
        armadas = request.env['cdn.armada'].sudo().search([('priority', '=', 1)])

        website = request.render('cdn_rental_armada.home_page', {
            'products': products, 
            'armadas': armadas
            })
        return website

    @http.route('/armada', auth='public', website=True)
    def index(self, **kw):
        armadas = request.env['cdn.armada'].sudo().search([('priority', '=', 1)])
        return request.render('cdn_rental_armada.armada_list', {'armadas': armadas})
        
    @http.route('/booking' , auth='public', website=True)
    def Produk(self, **kw):
        # products = request.env['cdn.produk.armada'].sudo().search([('priority', '=', '1')])
        # renderweb = request.render('cdn_rental_armada.product_booking', {'products': products})
        # return renderweb
        return "produk booking"
    
    
    @http.route('/test' , auth='public', website=True)
    def test(self, **kw):
        # products = request.env['cdn.produk.armada'].sudo().search([])
        return request.render('cdn_rental_armada.test_landing')
    