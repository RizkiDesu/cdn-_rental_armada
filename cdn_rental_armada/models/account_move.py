from odoo import _, api, fields, models



class AccountMove(models.Model):
    _inherit = 'account.move'
    # jenis_armada   = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
    pemesanan_id   = fields.Integer(string='ID Pemesanan')

class AccountMove(models.Model):
    _inherit = 'account.move.line'
    
    supir          = fields.Many2one(comodel_name='cdn.supir', string='Supir')
    tenaga_bantu   = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantu')
    armada_id      = fields.Many2one(comodel_name='cdn.armada', string='Armada')
    
    @api.onchange('jenis_armada')
    def _onchange_jenis_armada(self):
        if self.jenis_armada:
            self.order_line = [(5, 0, 0)]