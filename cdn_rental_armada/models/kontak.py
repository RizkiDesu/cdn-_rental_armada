from odoo import models, fields, api

# ian
class ResPartner(models.Model):
   _inherit = 'res.partner'

   pekerjaan     = fields.Selection(string='Pekerjaan', selection=[('supir', 'Supir'), ('tenaga_bantuan', 'Tenaga Bantuan')])
   jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[('l', 'Laki Laki'), ('p', 'Perempuan')])
   no_ktp        = fields.Char(string='No KTP')
   umur          = fields.Integer(string='Umur')
   is_menikah    = fields.Boolean(string='Menikah', default=False)
   status        = fields.Selection(string='Status', selection=[('aktif', 'Aktif'), ('nonaktif', 'Nonaktif'),], default="nonaktif")
   
   
   
