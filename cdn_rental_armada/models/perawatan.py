from odoo import _, api, fields, models


# Triadi
class CdnService(models.Model):
    _name = 'cdn.service'
    _description = 'Service'
    _rec_name = 'tanggal'
    
    
    armada_id = fields.Many2one(comodel_name='cdn.armada', string='Armada', required=True)
    tanggal = fields.Date(string='Tanggal service')
    jenis_service = fields.Char(string='Jenis Perawatan')
    harga = fields.Integer(string='Pengeluran')
    deskripsi = fields.Text(string='Deskripsi')
    
    # @api.model
    # def create(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Armada',
    #         'res_model': 'cdn.armada',
    #         'view_mode': 'form',
    #         'target': 'current',
    #     }
    # @api.model
    # def create(self, vals):
        
    #     # super(CdnService, self).create(vals)
        
    #     return 
    
