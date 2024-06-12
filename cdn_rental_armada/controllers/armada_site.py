import base64
from odoo import http
from odoo.http import request

class ArmadaSite(http.Controller):

    # ------------------------------ HOME ---------------------------------------------
    @http.route('/' , auth='public', website=True)
    def home(self, **kw):
        var ={
            'products': request.env['cdn.produk.armada'].sudo().search([('priority', '=', '1')]),
            'armadas': request.env['cdn.armada'].sudo().search([('priority', '=', 1)])
        }
        return request.render('cdn_rental_armada.home_page', var)

    # ------------------------------ ARMADA ---------------------------------------------
    @http.route('/armada', auth='public', website=True)
    def index(self, **kw):
        armadas = request.env['cdn.armada'].sudo().search([('priority', '=', 1)])
        return request.render('cdn_rental_armada.armada_list', {'armadas': armadas})
        



    # ------------------------------ BOOKING ---------------------------------------------
    @http.route('/form_booking' , auth='user', website=True)
    def Produk(self, **kw):
        var = {
            'provinsi': request.env['cdn.propinsi'].sudo().search([]),
            'provinsi_tujuan': request.env['cdn.propinsi'].sudo().search([]),
        }
        return request.render('cdn_rental_armada.form_booking_website', var)
    
    # ------------------------------ BOKING ASAL ---------------------------------------------
    # FILTER KOTA BY PROVINSI
    @http.route('/get_kota_by_provinsi', type='json', auth='public') 
    def get_kota_by_provinsi(self, provinsi_id):
        print(provinsi_id)
        kota_records = request.env['cdn.kota'].sudo().search([('propinsi_id', '=', int(provinsi_id))])
        kota_data = [{'id': kota.id, 'name': kota.name} for kota in kota_records]
        return {'status': 200, 'kota': kota_data}
        
    # FILTER KECAMATAN BY KOTA
    @http.route('/get_kecamatan_by_kota', type='json', auth='public') 
    def get_kecamatan_by_kota(self, kota_id):
        kecamatan_records = request.env['cdn.kecamatan'].sudo().search([('kota_id', '=', int(kota_id))])
        kecamatan_data = [{'id': kecamatan.id, 'name': kecamatan.name} for kecamatan in kecamatan_records]
        return {'status': 200, 'kecamatan': kecamatan_data}

    # FILTER DESA BY KECAMATAN
    @http.route('/get_desa_by_kecamatan', type='json', auth='public') 
    def get_desa_by_kecamatan(self, kecamatan_id):
        desa_records = request.env['cdn.desa'].sudo().search([('kecamatan_id', '=', int(kecamatan_id))])
        desa_data = [{'id': desa.id, 'name': desa.name} for desa in desa_records]
        return {'status': 200, 'desa': desa_data}
    
    # ------------------------------ BOOKING TUJUAN ---------------------------------------------
    # FILTER KOTA TUJUAN BY PROVINSI TUJUAN
    @http.route('/get_kota_by_provinsi_tujuan', type='json', auth='public') 
    def get_kota_by_provinsi_tujuan(self, provinsi_id):
        print(provinsi_id)
        kota_records = request.env['cdn.kota'].sudo().search([('propinsi_id', '=', int(provinsi_id))])
        kota_data = [{'id': kota.id, 'name': kota.name} for kota in kota_records]
        return {'status': 200, 'kota': kota_data}

    # FILTER KECAMATAN TUJUAN BY KOTA TUJUAN
    @http.route('/get_kecamatan_by_kota_tujuan', type='json', auth='public') 
    def get_kecamatan_by_kota_tujuan(self, kota_id):
        kecamatan_records = request.env['cdn.kecamatan'].sudo().search([('kota_id', '=', int(kota_id))])
        kecamatan_data = [{'id': kecamatan.id, 'name': kecamatan.name} for kecamatan in kecamatan_records]
        return {'status': 200, 'kecamatan': kecamatan_data}

    # FILTER DESA TUJUAN BY KECAMATAN TUJUAN
    @http.route('/get_desa_by_kecamatan_tujuan', type='json', auth='public') 
    def get_desa_by_kecamatan_tujuan(self, kecamatan_id):
        desa_records = request.env['cdn.desa'].sudo().search([('kecamatan_id', '=', int(kecamatan_id))])
        desa_data = [{'id': desa.id, 'name': desa.name} for desa in desa_records]
        return {'status': 200, 'desa': desa_data}
    
    # ------------------------------ BOOKING SAVE ---------------------------------------------
    @http.route('/booking_save', auth='user', website=True, csrf=False, methods=['POST'])
    def save_booking(self, **kw):
        print(kw) 
        # RESPON DARI KW
        # {
        # 'jenis_armada': 'travel', 
        # 'jmlh': '2', 
        # 'tanggal': '2024-06-12', 
        # 'durasi': '1', 
        # 'alamat-penjemputan': 'adsd', 
        # 'provinsi': '119', 
        # 'kota': '742', 'kecamatan': '10473', 
        # 'desa': '7857', 
        # 'alamat_tujuan': 'dasdasd', 
        # 'provinsi_tujuan': '115', 
        # 'kota_tujuan': '672', 
        # 'kecamatan_tujuan': '9176', 
        # 'desa_tujuan': '16112'
        #}
        partner_id = request.env['res.users'].browse(request.uid).partner_id
        print(partner_id.name)
        request.env['cdn.pemesanan'].sudo().create({
            'pelanggan_id'  : partner_id.id,
            'jenis_armada'  : kw.get('jenis_armada'),
            'jumlah_armada' : kw.get('jmlh'),
            'tanggal_dipakai': kw.get('tanggal'),
            'durasi'        : kw.get('durasi'),

            'tempat_jemput' : kw.get('alamat-penjemputan'),
            'propinsi'      : kw.get('provinsi'),
            'kota'          : kw.get('kota'),
            'kecamatan'     : kw.get('kecamatan'),
            'desa'          : kw.get('desa'),

            'tujuan'        : kw.get('alamat_tujuan'),
            'propinsi_tujuan': kw.get('provinsi_tujuan'),
            'kota_tujuan'   : kw.get('kota_tujuan'),
            'kecamatan_tujuan': kw.get('kecamatan_tujuan'),
            'desa_tujuan'   : kw.get('desa_tujuan'),
        })
        return request.redirect('/form_booking')




    # ------------------------------ DAFTAR FORM ---------------------------------------------
    @http.route('/form_daftar' , auth='public', website=True)
    def daftar(self, **kw):
        # buat_pelanggan = 
        return request.render('cdn_rental_armada.form_daftar_website',{})

    # ------------------------------ DAFTAR SAVE ---------------------------------------------
    @http.route('/daftar_save', auth='public', website=True, csrf=False, methods=['POST'])
    def save_person(self, **kw):
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