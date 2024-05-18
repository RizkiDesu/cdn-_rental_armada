from odoo import models, fields, api



class ResPartner(models.Model):
   _inherit = 'res.partner'

   pekerjaan_ids = fields.Many2many(comodel_name='cdn.pekerjaan', string='Pekerjaan')
   jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[('l', 'Laki Laki'), ('p', 'Perempuan'),])
   no_ktp        = fields.Integer(string='No KTP')
   umur          = fields.Integer(string='Umur')
   is_menikah    = fields.Boolean(string='Menikah', default=True)
   status        = fields.Boolean(string='Aktif', default=True)
   

class CdnPekerjaan(models.Model):
   _name        = 'cdn.pekerjaan'
   _description = 'Pekerjaan'

   name         = fields.Char(string='Pekerjaan', required=True)

class CdnSim(models.Model):
   _name         = 'cdn.sim'
   _description  = 'cdn.sim'

   name        = fields.Char(string='Nama')
   no_sim      = fields.Char(string='No Sim')
   jenis_sim   = fields.Selection(string='Jenis Sim', selection=[('a', 'Sim A'), ('b', 'Sim B')])
   partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
   
   
   
