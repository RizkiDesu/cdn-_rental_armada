from odoo import models, fields, api, _
from datetime import date, timedelta
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError

import qrcode
import base64
from io import BytesIO

# CREATED BY IAN
# -------------------------------------------- PEMESANAN ---------------------------------------------------------------
class CdnPemesanan(models.Model):
   _name        = 'cdn.pemesanan'
   _description = 'cdn.pemesanan'
   _inherit     = ['mail.thread', 'mail.activity.mixin']

   # -------------------------------------------- RELATION PELANGGAN --------------------------------------------
   pelanggan_id         = fields.Many2one(comodel_name='res.partner', string='Pelanggan', domain=[('type_orang','=','pelanggan')], tracking=True)
   no_ktp               = fields.Char(string='No KTP', related='pelanggan_id.no_ktp', tracking=True)
   jalan                = fields.Char(string='Alamat', related='pelanggan_id.street', tracking=True)
   kota                 = fields.Char(string='Kota', related='pelanggan_id.city', tracking=True)
   ponsel               = fields.Char(string='No Ponsel', related='pelanggan_id.mobile', tracking=True)
   email                = fields.Char(string='Email', related='pelanggan_id.email', tracking=True)
   jenis_kelamin        = fields.Selection(string='Jenis Kelamin', related='pelanggan_id.jenis_kelamin', tracking=True)
   umur                 = fields.Integer(string='Umur', related='pelanggan_id.umur', tracking=True)

   # -------------------------------------------- PENJEMPUTAN DAN TUJUAN -----------------------------------------
   waktu_penjemputan    = fields.Char('Waktu Penjemputan')
   tempat_jemput        = fields.Text(string='Tempat Penjemputan', tracking=True)
   wilayah_penjemputan  = fields.Char(string='Wilayah Penjemputan')
   wilayah_tujuan       = fields.Char(string='Wilayah Tujuan')
   tujuan               = fields.Text(string='Tempat Tujuan', tracking=True)
   # propinsi             = fields.Many2one(comodel_name='cdn.propinsi', string='Provinsi', tracking=True)
   # kota                 = fields.Many2one(comodel_name='cdn.kota', string='Kota', tracking=True)
   # kecamatan            = fields.Many2one(comodel_name='cdn.kecamatan', string='Kecamatan', tracking=True)
   # desa                 = fields.Many2one(comodel_name='cdn.desa', string='Desa', tracking=True)
   # propinsi_tujuan      = fields.Many2one(comodel_name='cdn.propinsi', string='Provinsi', tracking=True)
   # kota_tujuan          = fields.Many2one(comodel_name='cdn.kota', string='Kota', tracking=True)
   # kecamatan_tujuan     = fields.Many2one(comodel_name='cdn.kecamatan', string='Kecamatan')
   # desa_tujuan          = fields.Many2one(comodel_name='cdn.desa', string='Desa', tracking=True)

   # -------------------------------------------- JENIS ARMADA  --------------------------------------------
   jenis_armada         = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], tracking=True) 


   # -------------------------------------------- STATUS  --------------------------------------------   
   state                = fields.Selection(string='State', selection=[('draft', 'Draft'), 
                                                            ('berjalan','Sedang Berjalan'), 
                                                            ('selesai', 'Selesai')], default="draft", tracking=True)
   status_pembayaran    = fields.Selection(string='Status Pembayaran', related='invoice_id.payment_state',store=True, tracking=True)
   barcode_tdd          = fields.Binary('QR Code', attachment=True)


   # -------------------------------------------- DETAIL PEMESANAN  ------------------------------------
   name                 = fields.Char(string='No Referensi', tracking=True)
   product_id           = fields.Many2one(comodel_name='product.product', string='Produk', tracking=True)
   produk_ids           = fields.One2many(comodel_name='cdn.pemesanan.armada', inverse_name='produk_armada_pemesanan_id', string='Daftar Produk', ondelete="cascade", tracking=True)
   invoice_id           = fields.Many2one('account.move', copy=False, string='Invoice', tracking=True)
   tanggal_pemesanan    = fields.Date(string='Tanggal Pemesanan', default=date.today(), tracking=True)
   total_harga          = fields.Float(string='Total', compute='_compute_total', tracking=True)
   tanggal_dipakai      = fields.Date(string='Tanggal Pemakaian', tracking=True)
   durasi               = fields.Integer(string='Durasi Sewa / hari', help='Berapa lama?', default="1", tracking=True)
   tanggal_kembali      = fields.Date( string='Tanggal Kembali', tracking=True)
   jumlah_armada        = fields.Integer(string='Jumlah Pesanan Armada', default="1", help='Berapa banyak armada yang disewa?', tracking=True)
   
   # -------------------------------------------- KATAKAN PETA !!! ------------------------------------
   peta_penjemputan     = fields.Char(string='Peta Penjemputan', tracking=True)
   peta_tujuan          = fields.Char(string='Peta Tujuan', tracking=True)
   

   # -------------------------------------------- METHOD ---------------------------------------------------
   def tanda_tangan(self):
      data = 'tdd ala rizki desu'
      for record in self:
         qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
         qr.add_data(data)
         qr.make(fit=True)
         img = qr.make_image(fill='black', back_color='white')
         buffer = BytesIO()
         img.save(buffer, format="PNG")
         qr_code_image = base64.b64encode(buffer.getvalue())
         record.barcode_tdd = qr_code_image


   @api.onchange('durasi','tanggal_dipakai')
   def _onchange_tanggal_kembali(self):
      for rec in self:
            if rec.tanggal_dipakai and rec.durasi is not None:
                rec.tanggal_kembali = rec.tanggal_dipakai + relativedelta.relativedelta(days=rec.durasi)
            else:
                rec.tanggal_kembali = False
   @api.constrains('tanggal_dipakai')
   def _check_tanggal_dipakai(self):
        for rec in self:
            if rec.tanggal_dipakai and rec.tanggal_dipakai < date.today():
                raise ValidationError("Tanggal Dipakai tidak boleh minimal hari ini.")
   
   @api.depends('produk_ids.subtotal')
   def _compute_total(self):
      for rec in self:
         total = sum(bayar.subtotal for bayar in rec.produk_ids)
         rec.total_harga = total

   @api.model
   def create(self, vals):
      vals['name'] = self.env['ir.sequence'].next_by_code('cdn.pemesanan')
      rekaman = super(CdnPemesanan, self).create(vals)
      rekaman.status_pembayaran = 'not_paid'
      

      return rekaman

   def get_current_company(self):
      current_company = self.env.user.company_id
      return current_company

   # -------------------------------------------- ACTION BUTTON ---------------------------------------------------

   # -------------------------------------------- ACTION LIHAT INVOICE ---------------------------------------------------
   def action_state_lihat_invoice(self):
      invoice_id = self.env['account.move'].search([('pemesanan_id', '=', self.id)])
      return {
         'type': 'ir.actions.act_window',
         'name': 'Customer Invoice',
         'res_model': 'account.move',
         'view_mode': 'form',
         'res_id': invoice_id.id,
         'target': 'current',
      }

   # -------------------------------------------- ACTION STATE SELESAI ---------------------------------------------------
   def action_state_selesai(self):
      # hitung jumlah produk armada yang telah disewa
      count = self.env['cdn.pemesanan.armada'].search_count([('produk_armada_pemesanan_id', '=', self.id), ('state','=','disewa')])
      
      if count > 0:
         return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
               'title': 'Gagal Ubah Status',
               'type': 'danger',
               'message': 'Terdapat armada yang belum kembali',
               'sticky': False,
            }
         }
      else:
         self.state = 'selesai'

   # -------------------------------------------- ACTION STATE BUAT INVOICE ---------------------------------------------------
   def action_kirim_email(self):
      
      return
   def action_state_buat_invoice(self):
      """Method for creating invoice"""
      company = self.env.user.company_id
      if self.env['cdn.pemesanan.armada'].search([('produk_armada_pemesanan_id', '=', self.id)]):
         invoice_vals = {
            'move_type': 'out_invoice',
            'date': fields.Date.today(),
            'invoice_date': fields.Date.today(),
            'partner_id': self.pelanggan_id.id,
            'pemesanan_id': self.id,
            'invoice_line_ids': [],
         }
         for line in self.produk_ids:
               invoice_line_vals = {
                  'product_id': line.produk_id.id,
                  'quantity': self.durasi,
                  'price_unit': line.biaya_sewa,
                  'armada_id': line.armada_id.id,
                  'supir': line.supir.id,
                  'tenaga_bantu': line.tenaga_bantuan.id,
               }
               line.armada_id.state = 'dipakai'
               line.state = 'disewa'
               line.supir.state = 'perjalanan'
               line.tenaga_bantuan.state = 'perjalanan'
               invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

         invoice_id = self.env['account.move'].sudo().create(invoice_vals)
         self.invoice_id = invoice_id
         self.state = 'berjalan'
         # ------------------------ TEMPLATE EMAIL ----------------------------------------------
         # '<td class="invi" style="text-align: right;border: 1px solid white;border-collapse: collapse">'
         #                                    '<img t-att-src="image_data_uri(o.env.user.company_id.logo)" alt="Logo" border="0" width="100"/>'
         #                                '</td>'
         mail_content = _(
            '<div class="page">'
               '<div class="container">'
                     '<div class="header">'
                        '<table style="width: 100%%;">'
                           '<tbody>'
                                 '<tr>'
                                    '<td style="text-align: left; margin-bottom: 50px; border: 1px solid white; border-collapse: collapse;">'
                                       '<h1>%s</h1>'  # company.name
                                       '<p>%s</p>'  # company.street
                                    '</td>'
                                 '</tr>'
                           '</tbody>'
                        '</table>'
                     '</div>'
                     
                     '<div class="section" align="center">'
                        '<div class="section-header" style="background-color: #004e70; color: white; margin-bottom: 20px; padding: 8px"><b>Details Pelanggan</b></div>'
                        '<div class="section-content">'
                           '<table style="width: 100%%; border: 1px solid; border-collapse: collapse; margin-bottom: 50px;">'
                                 '<tbody>'
                                    '<tr>'
                                       '<td style="border: 1px solid white;">Nama Pelanggan</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.pelanggan_id.name
                                       '<td style="border: 1px solid white;">Umur</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.pelanggan_id.umur
                                    '</tr>'
                                    '<tr>'
                                       '<td style="border: 1px solid white;">Jenis Kelamin</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.pelanggan_id.jenis_kelamin
                                       '<td style="border: 1px solid white;">Alamat</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.pelanggan_id.street
                                    '</tr>'
                                    '<tr>'
                                       '<td style="border: 1px solid white;">Email</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.pelanggan_id.email
                                       '<td style="border: 1px solid white;">Telp</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.pelanggan_id.mobile
                                    '</tr>'
                                 '</tbody>'
                           '</table>'
                        '</div>'
                     '</div>'
                     
                     '<div class="section" align="center">'
                        '<div class="section-header" style="background-color: #004e70; color: white; margin-bottom: 20px;padding: 8px"><b>Detail Pemesanan</b></div>'
                        '<div class="section-content">'
                           '<table style="width: 100%%; border: 1px solid; border-collapse: collapse; margin-bottom: 50px;">'
                                 '<tbody>'
                                    '<tr>'
                                       '<td style="border: 1px solid white;">Jenis Kendaraan</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.jenis_armada
                                       '<td style="border: 1px solid white;">Tanggal Pemakaian</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.tanggal_dipakai
                                    '</tr>'
                                    '<tr>'
                                       '<td style="border: 1px solid white;">Tanggal Pemesanan</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.tanggal_pemesanan
                                       '<td style="border: 1px solid white;">Tanggal Kembali</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.tanggal_kembali
                                    '</tr>'
                                    '<tr>'
                                       '<td style="border: 1px solid white;">Total Biaya</td>'
                                       '<td style="border: 1px solid white;">: Rp. %s</td>'  # self.total_harga
                                       '<td style="border: 1px solid white;">Durasi Sewa</td>'
                                       '<td style="border: 1px solid white;">: %s Hari</td>'  # self.durasi
                                    '</tr>'
                                 '</tbody>'
                           '</table>'
                        '</div>'
                     '</div>'
                     
                     '<div class="section" align="center">'
                        '<div class="section-header" style="background-color: #004e70; color: white; margin-bottom: 20px; padding: 8px"><b>Penjemputan dan Tujuan</b></div>'
                        '<div class="section-content">'
                           '<table style="width: 100%%; border: 1px solid; border-collapse: collapse; margin-bottom: 50px;">'
                                 '<tbody >'
                                    '<tr>'
                                       '<td style="border: 1px solid white;">Alamat Penjemputan</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.tempat_jemput
                                       '<td style="border: 1px solid white;">Tujuan (jika ada)</td>'
                                       '<td style="border: 1px solid white;">: %s</td>'  # self.tujuan
                                    '</tr>'
                                 '</tbody>'
                           '</table>'
                        '</div>'
                     '</div>'
                     '<div class="section" align="center">'
                     '<div class="section-header" style="background-color: #004e70; color: white; margin-bottom: 20px; padding: 8px"><b>Detail Armada</b></div>'
                     '<div class="section-content">'
                        '%s'  # Details produk_ids placeholder
                        
                     '</div>'
                     '</div>'
                     
                     '<div class="section note">'
                        '<div class="section-header" style="background-color: #004e70; color: white; margin-bottom: 20px; padding: 8px"><b>Ketentuan - Ketentuan Persewaan Kendaraan :</b></div>'
                        '<div class="section-content">'
                           '<ul>'
                                 '<li>Kendaraan tersebut (yang disewakan) tidak dapat dipindah tangankan kepada pihak lain / kedua tanpa seizin pemilik kendaraan.</li>'
                                 '<li>Kendaraan tersebut diatas tidak dapat dijadikan jaminan/digadaikan dengan tujuan apapun kepada siapapun.</li>'
                                 '<li>Pelanggaran akan diproses melalui jalur pidana dan pemilik kendaraan berhak untuk mengambil kembali kendaraan apabila terjadi pelanggaran atau terdapat kejanggalan lainnya mengenai pemakaian kendaraan dimana hal ini dirasakan oleh pemilik kendaraan.</li>'
                                 '<li>Pengembalian kendaraan harus dalam keadaan seperti pada saat keluarnya surat ini, jika ada body tabrakan adalah tanggung jawab penyewa.</li>'
                           '</ul>'
                        '</div>'
                     '</div>'
               '</div>'
            '</div>'
         ) % (
            company.name, company.street, self.pelanggan_id.name, self.pelanggan_id.umur,
            self.pelanggan_id.jenis_kelamin, self.pelanggan_id.street, self.pelanggan_id.email,
            self.pelanggan_id.mobile, self.jenis_armada, self.tanggal_dipakai, self.tanggal_pemesanan,
            self.tanggal_kembali, self.total_harga, self.durasi, self.tempat_jemput, self.tujuan,
            ''.join([
               '<div class="section" align="center">'
                     '<div class="section-header" style="background-color: #004e70; color: white; margin-bottom: 20px; padding: 2px"><b></b></div>'
                     '<div class="section-content">'
                     
                        '<table style="width: 100%%; border: 1px solid grey; color : border-collapse: collapse; margin-bottom: 50px;">'
                           '<tbody>'
                              '<tr>'
                                 '<td style="border: 1px solid white;"><b>ID Armada</b></td>'
                                 '<td style="border: 1px solid white;">: <b>{}</b></td>' 
                                 '<td style="border: 1px solid white;"></td>' 
                                 '<td style="border: 1px solid white;">Sopir (jika ada)</td>'
                                 '<td style="border: 1px solid white;">: {}</td>'       
                              '</tr>'              
                              '<tr>'
                                 '<td style="border: 1px solid white;">Nopol dan Nama Armada</td>'
                                 '<td style="border: 1px solid white;">: {}</td>' 
                                 '<td style="border: 1px solid white;"></td>' 
                                 '<td style="border: 1px solid white;">Tenaga Bantu (jika ada)</td>'
                                 '<td style="border: 1px solid white;">: {}</td>'
                              '</tr>'
                        '</tbody>'
                     '</table>'
                        
                     '</div>'
                     '</div> <br></br><br></br>'
                     
               .format(line.id, line.supir.name, line.armada_id.name, line.tenaga_bantuan.name)
               for line in self.produk_ids
            ])
         )

         main_content = {
            'subject': "Permintaan Booking Disetujui",
            'author_id': self.env.user.partner_id.id,
            'body_html': mail_content,
            'email_to': self.pelanggan_id.email,
         }

         self.env['mail.mail'].create(main_content).send()

         return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
            'target': 'current',
         }
      else:
         raise ValidationError("Silahkan isi Produk Armada")


# CREATED BY IAN
# -------------------------------------------- PEMESANAN LINE ---------------------------------------------------------------
class CdnPemesananArmada(models.Model):

   _name          = 'cdn.pemesanan.armada'
   _description   = 'cdn.pemesanan.armada'
   _rec_name      = 'armada_id'
   
   # -------------------------------------------- ARMADA ----------------------------------------------------------------------------
   gambar_mobil               = fields.Image('Gambar', related='armada_id.foto_mobil') 
   armada_id                  = fields.Many2one(comodel_name='cdn.armada', string='Armada')
   
   # -------------------------------------------- RELATION PEMESANAN ---------------------------------------------------------------
   produk_armada_pemesanan_id = fields.Many2one(comodel_name='cdn.pemesanan', string='Armada Pemesanan')
   pelanggan_id               = fields.Many2one(related='produk_armada_pemesanan_id.pelanggan_id', store=True)
   produk_id                  = fields.Many2one(comodel_name='product.product', string='Produk', compute='_onchange_produk_armada_pemesanan_id', store=True)
   # produk_id                  = fields.Many2one(relate='produk_armada_pemesanan_id.product_id', store=True)
   supir                      = fields.Many2one(comodel_name='cdn.supir', string='Supir')
   tenaga_bantuan             = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantuan')

   # -------------------------------------------- DETAIL PEMESANAN -----------------------------------------------------------------
   biaya_sewa                 = fields.Float(string='Biaya Sewa/hari', related="produk_id.lst_price", store=True)
   subtotal                   = fields.Float(string='Subtotal', compute="_onchange_subtotal")
   invoice_denda              = fields.Many2one(comodel_name='account.move', string='Invoice Denda')
   status_pembayaran_denda    = fields.Selection(string='Status Pembayaran Denda', related='invoice_denda.payment_state')
   state                      = fields.Selection(string='Status Armada', selection=[('siap', 'Siap'), 
                                                                                 ('disewa', 'Disewa'), 
                                                                                 ('dikembalikan', 'Telah Kembali'), 
                                                                                 ('dikembalikan_denda', 'Telah Kembali (Denda)'),], 
                                                                                    default="siap")

                                                                                    
   @api.onchange('produk_armada_pemesanan_id','produk_armada_pemesanan_id.jenis_armada','product_id.product_id')
   def _onchange_produk_armada_pemesanan_id(self):
      for rec in self:
         rec.produk_id = rec.produk_armada_pemesanan_id.product_id.id

   @api.onchange('produk_id')
   def _onchange_subtotal(self):
      for rec in self:
         durasi = rec.produk_armada_pemesanan_id.durasi
         tot = durasi * rec.biaya_sewa
         rec.subtotal = tot
   
   def lihat_invoice_produk_armada_pemesanan(self) :
      for rec in self : 
         invoice_lines = self.env['account.move.line'].search([('produk_pemesanan_id','=',rec.id)])
         return {
            'type': 'ir.actions.act_window',
            'name': 'Tagihan Denda',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice_lines.move_id.id,
            'target': 'current',
         }