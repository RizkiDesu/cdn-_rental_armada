from odoo import _, api, fields, models 

# Triadi
class CdnPelanggan(models.Model):
    _name        = 'cdn.pelanggan'
    _description = 'Pelanggan'
    _inherits    = {'res.partner': 'partner_id'}

    # rizki
    jumlahbayar_ids = fields.One2many(comodel_name='cdn.pemesanan', inverse_name='pelanggan_id', string='invoice')
    total_bayar     =  fields.Float(string='total bayar', compute='_compute_total_bayar')

    def tombol_tagihan(self):
        action              = self.env["ir.actions.actions"]._for_xml_id("cdn_rental_armada.cdn_pemesanan_action")
        action['domain']    = [('pelanggan_id', '=', self.partner_id.id)]
        action['context']   = {'default_pelanggan_id': self.partner_id.id}
        return action

    @api.depends('jumlahbayar_ids.total_harga')
    def _compute_total_bayar(self):
        for rec in self:
            Jmlh            = self.env['cdn.pemesanan'].search([('pelanggan_id', '=', rec.partner_id.id)])
            rec.total_bayar = sum(bayar.total_harga for bayar in Jmlh)



