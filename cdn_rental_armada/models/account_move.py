from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move' 
    pemesanan_id   = fields.Integer(string='ID Pemesanan')
    tagihan_denda  = fields.Boolean(string='Tagihan Denda', default=False)

class AccountMove(models.Model):
    _inherit = 'account.move.line'
    
    supir                = fields.Many2one(comodel_name='cdn.supir', string='Supir')
    tenaga_bantu         = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantu')
    armada_id            = fields.Many2one(comodel_name='cdn.armada', string='Armada')
    jenis_armada         = fields.Selection(related='armada_id.jenis_armada')    
    produk_pemesanan_id  = fields.Many2one('cdn.pemesanan.armada', string='Produk Armada')
    
    
    
