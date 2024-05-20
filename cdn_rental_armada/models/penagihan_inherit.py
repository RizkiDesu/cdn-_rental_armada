from odoo import _, api, fields, models



class AccountMove(models.Model):
    _inherit = 'account.move'

    produk_id = fields.Many2one(comodel_name='product.template', string='Produk yamg di sewa')
    jenis_armada = fields.Selection(string='Jenis Kendaraan', related='produk_id.jenis_armada', store=True)

    supir_id = fields.Many2one(comodel_name='res.partner', string='supir', domain=[('pekerjaan', '=', 'supir')])
    tenagabantu_id = fields.Many2one(comodel_name='res.partner', string='Tenaga Bantu', domain=[('pekerjaan', '=', 'tenaga_bantuan')])