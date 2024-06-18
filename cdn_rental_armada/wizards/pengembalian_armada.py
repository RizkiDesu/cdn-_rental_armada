from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta

# CREATED BY IAN
# ------------------------------- PENGEMBALIAN ARMADA --------------------------------
class CdnPengembalianArmadaWizard(models.TransientModel):
   _name = 'cdn.pengembalian.armada.wizard'
   _description = 'cdn.pengembalian.armada.wizard'

   pemesanan_id            = fields.Many2one(comodel_name='cdn.pemesanan', string='Pesanan', domain="[('state','=','berjalan')]")
   produk_pemesanan_id     = fields.Many2one(comodel_name='cdn.pemesanan.armada', string='Armada', domain="[('state','=','disewa')]")
   armada_id               = fields.Many2one(comodel_name='cdn.armada', string='Armada', domain="[('state','=','dipakai')]")
   km_awal                 = fields.Float(string='KM Awal')
   km_akhir                = fields.Float(string='KM Akhir')
   jarak_tempuh            = fields.Float(string='Jarak Tempuh', compute="_compute_jarak_tempuh", store=True)
   keterangan              = fields.Text('keterangan')
   tujuan                  = fields.Text(string='Tujuan')
   durasi_hari             = fields.Integer(string='Durasi Sewa / hari')
   
   status_armada           = fields.Selection(string='Status Armada', selection=[('siap', 'Siap'), ('tidak_siap', 'Tidak Siap'),])
   denda                   = fields.Boolean(string='Denda')
   denda_rusak             = fields.Boolean(string='Denda Kerusakan')
   denda_telat             = fields.Boolean(string='Denda Terlambat Pengembalian')

   biaya_denda_telat       = fields.Float(string='Biaya Denda Keterlambatan')
   bagian_dalam            = fields.Boolean(string='Bagian Dalam')
   bagian_luar             = fields.Boolean(string='Bagian Luar')
   biaya_bagian_dalam      = fields.Float(string='Biaya Denda')
   biaya_bagian_luar       = fields.Float(string='Biaya Denda')
   keterangan_bagian_dalam = fields.Text(string='Keterangan Kerusakan')
   keterangan_bagian_luar  = fields.Text(string='Keterangan Kerusakan')

   @api.onchange('produk_pemesanan_id')
   def _produk_pemesanan_id(self):
      produk_armada = self.env['cdn.pemesanan.armada'].browse(self.produk_pemesanan_id.id)
      # pemesanan_id  = self.env['cdn.pemesanan'].browse(self.pemesanan_id.id)
      
      self.km_awal = produk_armada.armada_id.km_akhir
      self.durasi_hari = produk_armada.produk_armada_pemesanan_id.durasi
      self.tujuan      = produk_armada.produk_armada_pemesanan_id.tujuan

   @api.depends('km_akhir')
   def _compute_jarak_tempuh(self):
      self.jarak_tempuh = self.km_akhir - self.km_awal
   

   # @api.model
   def konfirmasi_pengembalian(self):
      # res = super(CdnPengembalianArmadaWizard, self).create(vals)
      res = self.env['cdn.pengembalian.armada.wizard'].create({
         'armada_id'                : self.armada_id.id,
         'keterangan'               : self.keterangan,
         'tujuan'                   : self.tujuan,
         'durasi_hari'              : self.durasi_hari,
         'km_awal'                  : self.km_awal,
         'km_akhir'                 : self.km_akhir,
         'jarak_tempuh'             : self.jarak_tempuh,
         'status_armada'            : self.status_armada,
         'denda'                    : self.denda,
         'denda_rusak'              : self.denda_rusak,
         'denda_telat'              : self.denda_telat,
         'biaya_denda_telat'        : self.biaya_denda_telat,
         'bagian_dalam'             : self.bagian_dalam,
         'bagian_luar'              : self.bagian_luar,
         'biaya_bagian_dalam'       : self.biaya_bagian_dalam,
         'biaya_bagian_luar'        : self.biaya_bagian_luar,
         'keterangan_bagian_dalam'  : self.keterangan_bagian_dalam,
         'keterangan_bagian_luar'   : self.keterangan_bagian_luar,
      })
      
      produk_armada = self.env['cdn.pemesanan.armada'].browse(self.produk_pemesanan_id.id)
      
      # set kilometer akhir dan state pada armada 
      produk_armada.armada_id.write({
         'km_akhir': res.km_akhir,
         'state': res.status_armada
      })

      # set state supir
      supir = self.env['cdn.supir'].search([('id', '=', produk_armada.supir.id)], limit=1)
      for rec in supir:
         rec.state = 'siap'

      # set state tenaga bantu
      tenaga_bantuan = self.env['cdn.tenaga.bantu'].search([('id', '=', produk_armada.tenaga_bantuan.id)], limit=1)
      for rec in tenaga_bantuan:
         rec.state = 'siap'

      # tambah histori armada
      self.env['cdn.history'].create({
         'armada_id' : produk_armada.armada_id.id,
         'jarak'     : res.jarak_tempuh,
         'km_akhir'  : res.km_akhir,
         'tgl_pakai' : date.today(),
         'tujuan'    : res.tujuan,
         'hari'      : res.durasi_hari,
      })

      if res.denda == True:
         invoice_vals = {
            'move_type'       : 'out_invoice',
            'tagihan_denda'   : True,
            'date'            : fields.Date.today(),
            'invoice_date'    : fields.Date.today(),
            'partner_id'      : produk_armada.produk_armada_pemesanan_id.pelanggan_id.id,
            'invoice_line_ids': [],
         }

         produk_id = self.env['product.product'].search([('default_code', '=', 'ref_produk_lain')], limit=1)
         if res.bagian_dalam == True:
            invoice_bagian_dalam_line = {
               'product_id': produk_id.id,
               'quantity'            : 1,
               'armada_id'           : produk_armada.armada_id.id,
               'name'                : res.keterangan_bagian_dalam,
               'produk_pemesanan_id' : produk_armada.id,
               'price_unit'          : res.biaya_bagian_dalam
            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_bagian_dalam_line))

         if res.bagian_luar == True:
            invoice_bagian_luar_line = {
               'product_id': produk_id.id,
               'quantity'            : 1,
               'armada_id'           : produk_armada.armada_id.id,
               'name'                : res.keterangan_bagian_luar,
               'price_unit'          : res.biaya_bagian_luar,
               'produk_pemesanan_id' : produk_armada.id,
            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_bagian_luar_line))

         if res.denda_telat == True:
            invoice_denda_telat_line = {
               'product_id': produk_id.id,
               'quantity'            : 1,
               'armada_id'           : produk_armada.armada_id.id,
               'name'                : 'Denda keterlambatan pengembalian armada',
               'price_unit'          : res.biaya_denda_telat,
               'produk_pemesanan_id' : produk_armada.id,
            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_denda_telat_line))

         invoice_id = self.env['account.move'].sudo().create(invoice_vals)

         produk_armada.state = 'dikembalikan_denda'
         produk_armada.invoice_denda = invoice_id

         return {
            'type'      : 'ir.actions.act_window',
            'name'      : 'Customer Invoice',
            'res_model' : 'account.move',
            'view_mode' : 'form',
            'res_id'    : invoice_id.id,
            'target'    : 'current',
         }
      else:
         produk_armada.state = 'dikembalikan'
         action_notification =  {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
               'title': 'Berhasil',
               'type': 'success',
               'message': 'Armada telah kembali',
               'sticky': False,
               'next' : {
                  'type': 'ir.actions.act_window_close'
               }
            }
         }
         
         return action_notification

         
      
   
