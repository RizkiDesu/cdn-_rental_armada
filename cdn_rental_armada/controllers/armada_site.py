import base64
from odoo import http
from odoo.http import request


# CREATED BY RIZKI
# --------------------------------- ARMADA SITE --------------------------------
class ArmadaSite(http.Controller):

    # ------------------------------ HOME ---------------------------------------------
    @http.route('/' , auth='public', website=True)
    def home(self, **kw):
        seting_id   = request.env['ir.config_parameter'].sudo().get_param('cdn_rental_armada.deskripsi_id')
        seting      = request.env['cdn.deskripsi'].sudo().search([('id', '=', seting_id)])
        var ={
            'title': request.env['ir.config_parameter'].sudo().get_param('cdn_rental_armada.slogan'),
            'title_description': seting.name,
            'deskripsi': seting.deskripsi,
            'services': request.env['cdn.your.service'].sudo().search([]),
            'consumers': request.env['cdn.pelanggan'].sudo().search([('priority', '=', '1')]),
            'products': request.env['product.product'].sudo().search([('priority', '=', '1')]),
            'armadas': request.env['cdn.armada'].sudo().search([('priority', '=', 1)]),
            # 'products': request.env['cdn.produk.armada'].sudo().search([('priority', '=', 1)])
        }
        return request.render('cdn_rental_armada.home_page', var)

    # ------------------------------ PRODUK ---------------------------------------------
    @http.route('/our_produk', auth='public', website=True)
    def product(self, **kw):
        products = request.env['product.product'].sudo().search([('jenis_armada','!=', False)])
        return request.render('cdn_rental_armada.our_produk', {'products': products})

    # ------------------------------ BOOKING BY PRODUK ------------------------------------
    @http.route('/form_booking/<int:product_id>', auth='user', website=True)
    def product_id(self, product_id,  **kw):
        produk_records = request.env['product.product'].sudo().browse(product_id)
        var = {
            'product' : produk_records,
            'provinsi_tujuan': request.env['cdn.propinsi'].sudo().search([]),
            'provinsi': request.env['cdn.propinsi'].sudo().search([])
        }
        return request.render('cdn_rental_armada.form_booking_website', var)


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

    #FILTER PRODUK BY JENIS ARMADA
    @http.route('/get_produk_by_jenis_armada', type='json', auth='public')
    def get_produk_by_jenis_armada(self, jenis_armada):
        produk_records = request.env['product.product'].sudo().search([('jenis_armada', '=', jenis_armada)])
        produk_data = [{'id': produk.id, 'name': produk.name} for produk in produk_records]
        return {'status': 200, 'produk': produk_data}

    #TAMPILKAN HARGA
    @http.route('/get_harga_by_product', type='json', auth='public')
    def get_harga_by_product(self, product_id):
        product = request.env['product.product'].sudo().search([('id', '=', int(product_id))])
        return {'status': 200, 'harga': product.lst_price}

    # ------------------------------ BOOKING SAVE ---------------------------------------------
    @http.route('/booking_save', auth='user', website=True, csrf=False, methods=['POST'])
    def save_booking(self, **kw):
        partner_id = request.env['res.users'].browse(request.uid).partner_id
        request.env['cdn.pemesanan'].sudo().create({
            'pelanggan_id'  : partner_id.id,
            'jenis_armada'  : kw.get('jenis_armada'),
            'jumlah_armada' : kw.get('jmlh'),
            'tanggal_dipakai': kw.get('tanggal'),
            'durasi'        : kw.get('durasi'),
            'product_id'    : kw.get('produk'),
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
        return request.redirect('/terimakasih/Booking')

    # ------------------------------ DAFTAR FORM ---------------------------------------------
    @http.route('/form_daftar', auth='public', website=True)
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
        return request.redirect('/terimakasih/booking')
    
    # ------------------------------ TERIMAKASIH PAGE -------------------------------------------
    @http.route('/terimakasih/<string:message>', auth='public', website=True)
    def terimakasih(self, message, **kwargs):
        var = {
            'message': message
        }
        return request.render('cdn_rental_armada.terimakasih_website', var)

    
