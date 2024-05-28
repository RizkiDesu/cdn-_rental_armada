from odoo import models, fields, api

# ian
class ResPartner(models.Model):
   _inherit       = 'res.partner'


   jenis_kelamin  = fields.Selection(string='Jenis Kelamin', selection=[('l', 'Laki Laki'), ('p', 'Perempuan')], tracking=True)
   no_ktp         = fields.Char(string='No KTP', tracking=True)
   umur           = fields.Integer(string='Umur', tracking=True)
   is_menikah     = fields.Boolean(string='Menikah', default=False, tracking=True)
   status         = fields.Selection(string='Status', selection=[('aktif', 'Aktif'), ('nonaktif', 'Nonaktif'),], default="nonaktif", tracking=True)
   type_orang     = fields.Selection(string='Tipe', selection=[('pelanggan', 'Pelanggan'), ('sopir', 'Sopir'),('tenaga_bantu', 'Tenaga bantu')], tracking=True)
   