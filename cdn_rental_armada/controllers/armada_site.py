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
    
    # ------------------------------ jemput ---------------------------------------------

    @http.route('/get_kota_by_provinsi', type='json', auth='public')
    def get_kota_by_provinsi(self, provinsi_id):
        print(provinsi_id)
        kota_records = request.env['cdn.kota'].sudo().search([('propinsi_id', '=', int(provinsi_id))])
        kota_data = [{'id': kota.id, 'name': kota.name} for kota in kota_records]
        return {'status': 200, 'kota': kota_data}

    @http.route('/get_kecamatan_by_kota', type='json', auth='public')
    def get_kecamatan_by_kota(self, kota_id):
        kecamatan_records = request.env['cdn.kecamatan'].sudo().search([('kota_id', '=', int(kota_id))])
        kecamatan_data = [{'id': kecamatan.id, 'name': kecamatan.name} for kecamatan in kecamatan_records]
        return {'status': 200, 'kecamatan': kecamatan_data}

    @http.route('/get_desa_by_kecamatan', type='json', auth='public')
    def get_desa_by_kecamatan(self, kecamatan_id):
        desa_records = request.env['cdn.desa'].sudo().search([('kecamatan_id', '=', int(kecamatan_id))])
        desa_data = [{'id': desa.id, 'name': desa.name} for desa in desa_records]
        return {'status': 200, 'desa': desa_data}
    

    # -------------------- tujuan ----------------------------------------------


    @http.route('/get_kota_by_provinsi_tujuan', type='json', auth='public')
    def get_kota_by_provinsi_tujuan(self, provinsi_id):
        print(provinsi_id)
        kota_records = request.env['cdn.kota'].sudo().search([('propinsi_id', '=', int(provinsi_id))])
        kota_data = [{'id': kota.id, 'name': kota.name} for kota in kota_records]
        return {'status': 200, 'kota': kota_data}

    @http.route('/get_kecamatan_by_kota_tujuan', type='json', auth='public')
    def get_kecamatan_by_kota_tujuan(self, kota_id):
        kecamatan_records = request.env['cdn.kecamatan'].sudo().search([('kota_id', '=', int(kota_id))])
        kecamatan_data = [{'id': kecamatan.id, 'name': kecamatan.name} for kecamatan in kecamatan_records]
        return {'status': 200, 'kecamatan': kecamatan_data}

    @http.route('/get_desa_by_kecamatan_tujuan', type='json', auth='public')
    def get_desa_by_kecamatan_tujuan(self, kecamatan_id):
        desa_records = request.env['cdn.desa'].sudo().search([('kecamatan_id', '=', int(kecamatan_id))])
        desa_data = [{'id': desa.id, 'name': desa.name} for desa in desa_records]
        return {'status': 200, 'desa': desa_data}
    


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