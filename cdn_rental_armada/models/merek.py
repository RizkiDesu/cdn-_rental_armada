from odoo import _, api, fields, models

class CdnMerek(models.Model):
    _name = 'cdn.merek'
    _description = 'Merek'
    
    name = fields.Char(string='Nama', required=True)
    jenis_ids = fields.One2many(comodel_name='cdn.jenis.kendaraan', inverse_name='merek_id', string='Jenis Kendaraan')
    
    
    
