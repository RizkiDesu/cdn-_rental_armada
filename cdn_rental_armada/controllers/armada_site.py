import base64
from odoo import http
from odoo.http import request

class ArmadaSite(http.Controller):
    @http.route('/' , auth='public', website=True)
    def home(self, **kw):
        var ={
            'products': request.env['cdn.produk.armada'].sudo().search([('priority', '=', '1')]),
            'armadas': request.env['cdn.armada'].sudo().search([('priority', '=', 1)])
        }
        return request.render('cdn_rental_armada.home_page', var)

    @http.route('/armada', auth='public', website=True)
    def index(self, **kw):
        armadas = request.env['cdn.armada'].sudo().search([('priority', '=', 1)])
        return request.render('cdn_rental_armada.armada_list', {'armadas': armadas})
        

    @http.route('/form_booking' , auth='public', website=True)
    def Produk(self, **kw):
        var = {
            'provinsi': request.env['cdn.propinsi'].sudo().search([]),
            'kota': request.env['cdn.kota'].sudo().search([]),
            'kecamatan': request.env['cdn.kecamatan'].sudo().search([]),
            'desa': request.env['cdn.desa'].sudo().search([]),

            
            'provinsi_tujuan': request.env['cdn.propinsi'].sudo().search([]),
            'kota_tujuan': request.env['cdn.kota'].sudo().search([]),
            'kecamatan_tujuan': request.env['cdn.kecamatan'].sudo().search([]),
            'desa_tujuan': request.env['cdn.desa'].sudo().search([])

        }
        return request.render('cdn_rental_armada.form_booking_website', var)

    @http.route('/booking_save', auth='public', website=True, csrf=False, methods=['POST'])
    def save_booking(self, **kw):
        return request.redirect('/form_daftar')
        











    @http.route('/form_daftar' , auth='public', website=True)
    def daftar(self, **kw):
        # buat_pelanggan = 
        return request.render('cdn_rental_armada.form_daftar_website',{})

    @http.route('/daftar_save', auth='public', website=True, csrf=False, methods=['POST'])
    def save_person(self, **kw):
        # image = request.httprequest.files.get('image')
        # image_base64 = base64.b64encode(image.read()) if image else False
        # print(kw)
        
        # {'nama': 'dsfsdf', 
        # 'ktp': 'fsfsf', 
        # 'telepon': 'sfs', 
        # 'email': 's4y4pu1an6@gmail.com', 
        # 'kelamin': 'Laki - Laki', 
        # 'umur': '435', 
        # 'status': 'Menikah', 
        # 'alamat': 'Dusun Kutukan Rt 03/ Rw 02 Desa Rejosari, Kecamantan Bantur, Kab. Malang, Jawa Timur'}

        request.env['cdn.pelanggan'].sudo().create({
            'name': kw.get('nama'),
            'email': kw.get('email'),
            'umur': kw.get('umur'),
            'street': kw.get('alamat'),
            'no_ktp': kw.get('ktp'),
            'is_menikah': kw.get('status'),
            'jenis_kelamin': kw.get('kelamin'),
            'mobile': kw.get('telepon'),
            'type_orang' : 'pelanggan',
        })
        return request.redirect('/form_daftar')