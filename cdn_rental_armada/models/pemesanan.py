from odoo import models, fields, api, _
from datetime import date
from dateutil import relativedelta

class CdnPemesanan(models.Model):
   _name        = 'cdn.pemesanan'
   _description = 'cdn.pemesanan'

   state                = fields.Selection(string='State', selection=[('draft', 'Draft'), ('terekam', 'Terekam')], default="draft")
   status_pembayaran    = fields.Selection(string='State', selection=[('belum_lunas', 'Belum Lunas'), ('lunas', 'Lunas')], default="belum_lunas")
   name                 = fields.Char(string='No Referensi')
   pelanggan_id         = fields.Many2one(comodel_name='res.partner', string='Pelanggan', domain=[('type_orang','=','pelanggan')])
   no_ktp               = fields.Char(string='No KTP', related='pelanggan_id.no_ktp')
   jalan                = fields.Char(string='Alamat', related='pelanggan_id.street')
   kota                 = fields.Char(string='Kota', related='pelanggan_id.city')
   ponsel               = fields.Char(string='No Ponsel', related='pelanggan_id.mobile')
   email                = fields.Char(string='Email', related='pelanggan_id.email')
   jenis_kelamin        = fields.Selection(string='Jenis Kelamin', related='pelanggan_id.jenis_kelamin')
   umur                 = fields.Integer(string='Umur', related='pelanggan_id.umur')
   tanggal_pemesanan    = fields.Date(string='Tanggal Pemesanan', default=date.today())
   produk_ids           = fields.One2many(comodel_name='cdn.pemesanan.armada', inverse_name='produk_armada_pemesanan_id', string='Daftar Produk')
   # produk_id            = fields.Many2one(comodel_name='product.product', string='Produk')
   # lst_price            = fields.Float(string='Harga Sewa/hari', related="produk_id.lst_price")
   # tanggal_pengembalian = fields.Date(string='Tanggal Pemesanan')

   def action_state_buat_invoice(self):
      for rec in self:
         rec.state = 'terekam'

   # @api.onchange('durasi_sewa', 'tanggal_pemesanan')
   # def _tgl_pengembalian(self):
   #    for rec in self:
   #       tanggal_pemesanan = rec.tanggal_pemesanan
   #       rec.tanggal_pengembalian = tanggal_pemesanan + relativedelta.relativedelta(days=rec.durasi_sewa)

class CdnPemesananArmada(models.Model):
   _name        = 'cdn.pemesanan.armada'
   _description = 'cdn.pemesanan.armada'

   produk_armada_pemesanan_id = fields.Many2one(comodel_name='cdn.pemesanan', string='Armada Pemesanan')
   produk_id                  = fields.Many2one(comodel_name='product.product', string='Produk')
   armada_id                  = fields.Many2one(comodel_name='cdn.armada', string='Armada')
   jenis_armada               = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
   supir                      = fields.Many2one(comodel_name='cdn.supir', string='Supir')
   tenaga_bantuan             = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantuan')
   durasi_sewa                = fields.Integer(string='Durasi Sewa/hari', default="1")
   biaya_sewa                 = fields.Float(string='Biaya Sewa/hari', related="produk_id.lst_price", store=True)
   kilometer_awal             = fields.Float(string='KM Awal')
   kilometer_akhir            = fields.Float(string='KM Akhir')
   jarak_tempuh               = fields.Float(string='Jarak Tempuh')
   tujuan                     = fields.Char(string='Tujuan')
   subtotal                   = fields.Float(string='Subtotal', compute="_onchange_subtotal")
   
   @api.onchange('durasi_sewa')
   def _onchange_subtotal(self):
      for rec in self:
         rec.subtotal = rec.durasi_sewa * rec.biaya_sewa
