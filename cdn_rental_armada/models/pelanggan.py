from odoo import _, api, fields, models 

# Triadi
class CdnPelanggan(models.Model):
    _name        = 'cdn.pelanggan'
    _description = 'Pelanggan'
    _inherits    = {'res.partner': 'partner_id'}
    _inherit     = ['mail.thread', 'mail.activity.mixin']
   

    # rizki
    jumlahbayar_ids = fields.One2many(comodel_name='account.move.line', inverse_name='partner_id', string='invoice')
    total_bayar = fields.Float(string='Total Bayar', compute='_compute_total_bayar')
    total_residual = fields.Float(string='Total Residual', compute='_compute_total_residual')

    @api.depends('jumlahbayar_ids')
    def _compute_total_residual(self):
        for rec in self:
            Jmlh            = self.env['account.move'].search([('partner_id', '=', rec.partner_id.id)])
            print(Jmlh)
            rec.total_residual = sum(bayar.amount_residual for bayar in Jmlh)

    @api.depends('jumlahbayar_ids')
    def _compute_total_bayar(self):
        for rec in self:
            Jmlh            = self.env['account.move'].search([('partner_id', '=', rec.partner_id.id)])
            # print(Jmlh)
            rec.total_bayar = sum(bayar.amount_untaxed for bayar in Jmlh)

    
    def tombol_tagihan(self):
        action              = self.env["ir.actions.actions"]._for_xml_id('account.action_move_out_invoice_type')
        action['view_mode'] = 'tree,form'
        action['domain']    = [('partner_id', '=', self.partner_id.id), ('move_type', '=', 'out_invoice')]
        action['context']   = {'default_partner_id': self.partner_id.id, 'default_move_type': 'out_invoice'}
        return action

    # @api.depends('jumlahbayar_ids.amount_total', 'jumlahbayar_ids.amount_residual')
    # def _compute_total_invoice(self):
    #     for rec in self:
    #         rec.total_invoice  = sum(rec.jumlahbayar_ids.mapped('amount_total'))
    #         rec.total_residual = sum(rec.jumlahbayar_ids.mapped('amount_residual'))




