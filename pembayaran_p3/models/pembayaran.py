# -*- coding: utf-8 -*-

from odoo import models, fields


class pembayaran(models.Model):
    _name           = 'pembayaran_p3.pembayaran'
    _description    = 'Pembayaran'
    _rec_name       = 'virtual_account'

    STATES          = [
        ('pending',         'Pending'),
        ('successfully',    'Berhasil'),
        ('failed',          'Gagal')
    ]

    READONLY_STATES = {
        'pending'       : [('readonly', False)],
        'failed'        : [('readonly', True)],
        'successfully'  : [('readonly', True)],
    }

    currency_id     = fields.Many2one('res.currency', string='Mata Uang', default=lambda self: self.env.user.company_id.currency_id.id)

    state           = fields.Selection(selection=STATES, string='Status', default='pending')

    virtual_account = fields.Char(string='No Referensi', required=True, states=READONLY_STATES)
    amount          = fields.Monetary(string='Total', required=True, states=READONLY_STATES)
    exp_date        = fields.Date(string='Tanggal Kadaluarsa', required=True, states=READONLY_STATES)
    description     = fields.Text(string='Deskripsi', required=True, states=READONLY_STATES)

    # hasil pembayaran
    url             = fields.Char(string='URL', states=READONLY_STATES)
    kode_pengesahan = fields.Char(string='Kode Pengesahan', states=READONLY_STATES)
    request         = fields.Text(string='Request', states=READONLY_STATES)
    response        = fields.Text(string='Response', states=READONLY_STATES)

    def action_open_wizard_bayar(self):
        return {
            'type'          : 'ir.actions.act_window',
            'res_model'     : 'pembayaran_p3.wizard_bayar',
            'view_mode'     : 'form',
            'view_id'       : self.env.ref('pembayaran_p3.wizard_bayar').id,
            'views'         : [(False, 'form')],
            'target'        : 'new',
            'context'       : "{'pembayaran_id': "+ str(self.id) +"}",
        }