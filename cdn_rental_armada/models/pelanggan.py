from odoo import _, api, fields, models 
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

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
    boking_ids = fields.One2many(comodel_name='cdn.pemesanan', inverse_name='pelanggan_id', string='Boking')
    status = fields.Selection(string='Status', selection=[('terdaftar', 'Terdaftar'), ('tidak_terdaftar', 'Belum Terdaftar'),], default="tidak_terdaftar")
    jml_boking = fields.Integer(string='Jumlah Boking', compute='_compute_jml_boking')
    
    def konfirmasi_web(self):
        portal_group = self.env.ref('base.group_portal')
        user_model = self.env['res.users']
        for rec in self:
            existing_user = user_model.search([('login', '=', rec.no_ktp)], limit=1)
            if existing_user:
                raise ValidationError("Pengguna dengan nomor KTP %s Sudah Terdaftar.", rec.no_ktp)
                continue

            # Create a new user
            new_user = user_model.create({
                'name': rec.name,
                'login': rec.email,
                'email': rec.email,
                'password': rec.no_ktp,
                'groups_id': [(6, 0, [portal_group.id])],
            })

            # Log the creation of the new user
            _logger.info('Created new portal user %s with email %s.', new_user.name, new_user.email)

            # Update the status
            rec.status = 'terdaftar'
        return True
    
    @api.depends('boking_ids')
    def _compute_jml_boking(self):
        for rec in self:
            jml = self.env['cdn.pemesanan'].search([('pelanggan_id', '=', rec.partner_id.id)])
            rec.jml_boking = len(jml)

    @api.depends('jumlahbayar_ids')
    def _compute_total_residual(self):
        for rec in self:
            Jmlh            = self.env['account.move'].search([('partner_id', '=', rec.partner_id.id)])
            rec.total_residual = sum(bayar.amount_residual for bayar in Jmlh)

    @api.depends('jumlahbayar_ids')
    def _compute_total_bayar(self):
        for rec in self:
            Jmlh            = self.env['account.move'].search([('partner_id', '=', rec.partner_id.id)])
            rec.total_bayar = sum(bayar.amount_untaxed for bayar in Jmlh)

    def tombol_tagihan(self):
        action              = self.env["ir.actions.actions"]._for_xml_id('account.action_move_out_invoice_type')
        action['view_mode'] = 'tree,form'
        action['domain']    = [('partner_id', '=', self.partner_id.id), ('move_type', '=', 'out_invoice')]
        action['context']   = {'default_partner_id': self.partner_id.id, 'default_move_type': 'out_invoice'}
        return action
    
    def tombol_booking(self):
        action              = self.env["ir.actions.actions"]._for_xml_id('cdn_rental_armada.cdn_pemesanan_action')
        action['view_mode'] = 'tree,form'
        action['domain']    = [('pelanggan_id', '=', self.partner_id.id)]
        action['context']   = {'default_pelanggan_id': self.partner_id.id}
        return action




