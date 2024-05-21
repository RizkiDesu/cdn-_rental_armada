from odoo import models, fields, api

# ian
class ResPartner(models.Model):
   _inherit = 'res.partner'

   pekerjaan     = fields.Selection(string='Pekerjaan', selection=[('supir', 'Supir'), ('tenaga_bantuan', 'Tenaga Bantuan')], required=True)
   jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[('l', 'Laki Laki'), ('p', 'Perempuan')], required=True)
   no_ktp        = fields.Char(string='No KTP', required=True)
   umur          = fields.Integer(string='Umur', required=True)
   is_menikah    = fields.Boolean(string='Menikah', default=False, required=True)
   status        = fields.Selection(string='Status', selection=[('aktif', 'Aktif'), ('nonaktif', 'Nonaktif'),], default="aktif", required=True)
   
   
