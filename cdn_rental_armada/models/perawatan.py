from odoo import _, api, fields, models



class CdnService(models.Model):
    _name = 'cdn.service'
    _description = 'Service'
    _rec_name = 'tanggal'
    
    
    armada_id = fields.Many2one(comodel_name='cdn.armada', string='Armada', required=True)
    tanggal = fields.Date(string='Tanggal service')
    jenis_service = fields.Char(string='Jenis Perawatan')
    harga = fields.Integer(string='Pengeluran')
    deskripsi = fields.Text(string='Deskripsi')
    
    
    
    
