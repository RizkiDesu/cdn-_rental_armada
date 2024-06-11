# -*- coding: utf-8 -*-

from odoo import models, fields
import requests
import random
import string
import json


class wizardBayar(models.Model):
    _name           = 'pembayaran_p3.wizard_bayar'
    _description    = 'Wizard Bayar'

    pembayaran_id   = fields.Many2one(string='Pembayaran', comodel_name='pembayaran_p3.pembayaran', required=True, default=lambda self: self.env.context.get('pembayaran_id', False), ondelete='cascade')
    url             = fields.Char(string='URL', required=True)

    def action_bayar(self):
        for rec in self:
            data            = {
                'virtual_account'   : rec.pembayaran_id.virtual_account,
                'amount'            : rec.pembayaran_id.amount,
                'date'              : fields.Date.today().strftime('%Y-%m-%d %H:%M:%S'),
                'kode_pengesahan'   : ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
            }

            headers         = {
                'Content-Type'  : 'application/json'
            }

            url             = rec.url
            response        = requests.post(
                url     = url,
                headers = headers,
                json    = data
            )

            if not str(response.headers.get('Content-Type')).startswith('application/json'):
                raise Exception('Invalid JSON response')

            result          = response.json()

            rec.pembayaran_id.write({
                'state'             : 'successfully' if result['is_success'] else 'failed',
                'request'           : data,
                'url'               : url,
                'kode_pengesahan'   : data['kode_pengesahan'],
                'response'          : json.dumps(result)
            })