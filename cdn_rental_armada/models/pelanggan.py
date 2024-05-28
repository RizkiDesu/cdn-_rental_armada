from odoo import _, api, fields, models 

# Triadi
class CdnPelanggan(models.Model):
    _name        = 'cdn.pelanggan'
    _description = 'Pelanggan'
    _inherits    = {'res.partner': 'partner_id'}

    # rizki
    jumlahbayar_ids = fields.One2many(comodel_name='account.move', inverse_name='partner_id', string='invoice')
    # total_invoice   = fields.Fload(string='total bayar')
    # total_residual  = fields.Float(string='sisa bayar')
    
    def tombol_tagihan(self):
        action              = self.env["ir.actions.actions"]._for_xml_id('account.action_move_out_invoice_type')
        action['view_mode'] = 'tree,form'
        action['domain']    = [('partner_id', '=', self.partner_id.id),('move_type', '=', 'out_invoice')]
        action['context']   = {'default_partner_id': self.partner_id.id , 'default_move_type': 'out_invoice'}
        return action

    # @api.depends('jumlahbayar_ids.amount_total', 'jumlahbayar_ids.amount_residual')
    # def _compute_total_invoice(self):
    #     for rec in self:
    #         rec.total_invoice  = sum(rec.jumlahbayar_ids.mapped('amount_total'))
    #         rec.total_residual = sum(rec.jumlahbayar_ids.mapped('amount_residual'))




