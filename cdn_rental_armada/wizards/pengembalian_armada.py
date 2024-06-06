from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta

class CdnPengembalianArmadaWizard(models.TransientModel):
   _name = 'cdn.pengembalian.armada.wizard'
   _description = 'cdn.pengembalian.armada.wizard'

   pesanan_id   = fields.Many2one(string='No Pesanan', comodel_name="cdn.pemesanan", domain="[('state','=','terekam')]")    
   armada_id    = fields.Many2one(comodel_name='cdn.armada', string='Armada', domain="[('state','=','dipakai')]")
   km_awal      = fields.Float(string='KM Awal')
   km_akhir     = fields.Float(string='KM Akhir')
   jarak_tempuh = fields.Float(string='Jarak Tempuh', compute="_compute_jarak_tempuh")
   keterangan   = fields.Text('keterangan')
   tujuan       = fields.Char(string='Tujuan')
   durasi_hari  = fields.Integer(string='Durasi Sewa / hari')
   
   status_armada = fields.Selection(string='Status Armada', selection=[('siap', 'Siap'), ('tidak_siap', 'Tidak Siap'),])
   
   @api.onchange('armada_id')
   def _onchange_armada_id(self):
      produk_armada = self.env['cdn.pemesanan.armada'].search([('armada_id', '=', self.armada_id.id)], limit=1)
      pemesanan_id  = self.env['cdn.pemesanan'].search([('id','=',produk_armada.produk_armada_pemesanan_id.id)], limit=1)
      
      print(pemesanan_id)
      print(pemesanan_id.durasi)
      print(pemesanan_id.tujuan)
      self.km_awal     = produk_armada.kilometer_awal
      self.durasi_hari = pemesanan_id.durasi
      self.tujuan      = pemesanan_id.tujuan

   @api.depends('km_akhir')
   def _compute_jarak_tempuh(self):
      self.jarak_tempuh = self.km_akhir - self.km_awal
   

   @api.model
   def create(self, vals):
      res = super(CdnPengembalianArmadaWizard, self).create(vals)

      produk_armada = self.env['cdn.pemesanan.armada'].search([('armada_id', '=', res.armada_id.id)], limit=1)
      for rec in produk_armada:
         rec.write({
            'kilometer_akhir': res.km_akhir,
            'jarak_tempuh': res.jarak_tempuh,
            'state': 'dikembalikan'
         })

      armada = self.env['cdn.armada'].search([('id', '=', res.armada_id.id)], limit=1)
      for rec in armada:
         rec.write({
            'km_akhir': armada.km_akhir + res.jarak_tempuh,
            'state': res.status_armada
         })

      supir = self.env['cdn.supir'].search([('id', '=', produk_armada.supir.id)], limit=1)
      for rec in supir:
         rec.write({
            'state': 'siap'
         })

      tenaga_bantuan = self.env['cdn.tenaga.bantu'].search([('id', '=', produk_armada.tenaga_bantuan.id)], limit=1)
      for rec in tenaga_bantuan:
         rec.write({
            'state': 'siap'
         })

      self.env['cdn.history'].create({
         'armada_id': res.armada_id.id,
         'jarak': res.jarak_tempuh,
         'km_akhir': res.km_akhir,
         'tgl_pakai': date.today(),
         'tujuan': res.tujuan,
         'hari': res.durasi_hari,
      })


      return res