from odoo import models, fields, api, _
from datetime import date
from dateutil import relativedelta
from odoo.exceptions import ValidationError
import http.client

class CdnPemesanan(models.Model):
   _name        = 'cdn.pemesanan'
   _description = 'cdn.pemesanan'

   state                = fields.Selection(string='State', selection=[('draft', 'Draft'), ('terekam', 'Terekam')], default="draft")
   # status_pembayaran    = fields.Selection(string='State', selection=[('belum_lunas', 'Belum Lunas'), ('lunas', 'Lunas')], default="belum_lunas")
   name                 = fields.Char(string='No Referensi')


   pelanggan_id         = fields.Many2one(comodel_name='res.partner', string='Pelanggan', domain=[('type_orang','=','pelanggan')])
   # pelanggan_id         = fields.Many2one(comodel_name='cdn.pelanggan', string='Pelanggan', domain=[('type_orang','=','pelanggan')])

   no_ktp               = fields.Char(string='No KTP', related='pelanggan_id.no_ktp')
   jalan                = fields.Char(string='Alamat', related='pelanggan_id.street')
   kota                 = fields.Char(string='Kota', related='pelanggan_id.city')
   ponsel               = fields.Char(string='No Ponsel', related='pelanggan_id.mobile')
   email                = fields.Char(string='Email', related='pelanggan_id.email')
   jenis_kelamin        = fields.Selection(string='Jenis Kelamin', related='pelanggan_id.jenis_kelamin')
   umur                 = fields.Integer(string='Umur', related='pelanggan_id.umur')
   tanggal_pemesanan    = fields.Date(string='Tanggal Pemesanan', default=date.today())
   produk_ids           = fields.One2many(comodel_name='cdn.pemesanan.armada', inverse_name='produk_armada_pemesanan_id', string='Daftar Produk')

   invoice_id           = fields.Many2one('account.move', copy=False, string='Invoice')
   total_harga          = fields.Float(string='Total', compute='_compute_total')
   tanggal_dipakai      = fields.Date(string='Tanggal Pemakaian')
   propinsi             = fields.Many2one(comodel_name='cdn.propinsi', string='Provinsi')
   kota                 = fields.Many2one(comodel_name='cdn.kota', string='Kota')
   kecamatan            = fields.Many2one(comodel_name='cdn.kecamatan', string='Kecamatan')
   desa                 = fields.Many2one(comodel_name='cdn.desa', string='Desa')
   propinsi_tujuan      = fields.Many2one(comodel_name='cdn.propinsi', string='Provinsi')
   kota_tujuan          = fields.Many2one(comodel_name='cdn.kota', string='Kota')
   kecamatan_tujuan     = fields.Many2one(comodel_name='cdn.kecamatan', string='Kecamatan')
   desa_tujuan          = fields.Many2one(comodel_name='cdn.desa', string='Desa')
   tempat_jemput        = fields.Text(string='Tempat Penjemputan')
   tujuan               = fields.Text(string='Tempat Tujuan')
   durasi               = fields.Integer(string='Durasi Sewa / hari', help='Berapa lama?', default="1")
   tanggal_kembali      = fields.Date( string='Tanggal Kembali')
   jenis_armada         = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
   status_pembayaran    = fields.Selection(string='Status Pembayaran', related='invoice_id.payment_state',store=True)
   
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
   def action_state_buat_invoice(self):
      """Method for creating invoice"""
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

         self.invoice_id = self.env['account.move'].sudo().create(invoice_vals)
         self.state = 'terekam'
         
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
      
   def get_current_company(self):
      current_company = self.env.user.company_id
      return current_company
   
class CdnPemesananArmada(models.Model):
   _name        = 'cdn.pemesanan.armada'
   _description = 'cdn.pemesanan.armada'
   # _rec_name = 'produk_armada_pemesanan_id'
   
   pelanggan_id               = fields.Many2one(related='produk_armada_pemesanan_id.pelanggan_id', store=True)
   produk_armada_pemesanan_id = fields.Many2one(comodel_name='cdn.pemesanan', string='Armada Pemesanan')
   produk_id                  = fields.Many2one(comodel_name='product.product', string='Produk')
   armada_id                  = fields.Many2one(comodel_name='cdn.armada', string='Armada')
   supir                      = fields.Many2one(comodel_name='cdn.supir', string='Supir')
   tenaga_bantuan             = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantuan')
   biaya_sewa                 = fields.Float(string='Biaya Sewa/hari', related="produk_id.lst_price", store=True)
   kilometer_awal             = fields.Float(string='KM Awal', related='armada_id.km_akhir')
   kilometer_akhir            = fields.Float(string='KM Akhir')
   jarak_tempuh               = fields.Float(string='Jarak Tempuh')
   tujuan                     = fields.Char(string='Tujuan')
   subtotal                   = fields.Float(string='Subtotal', compute="_onchange_subtotal")
   state                      = fields.Selection(string='Status Armada', selection=[('siap', 'Siap'), ('disewa', 'Disewa'), ('dikembalikan', 'Telah Kembali'),], default="siap")
   gambar_mobil               = fields.Image('Gambar', related='armada_id.foto_mobil') 
   
   @api.onchange('produk_id')
   def _onchange_subtotal(self):
      for rec in self:
         durasi = rec.produk_armada_pemesanan_id.durasi
         tot = durasi * rec.biaya_sewa 
         rec.subtotal = tot
