from odoo import _, api, fields, models 

# Triadi
class CdnPelanggan(models.Model):
    _name        = 'cdn.pelanggan'
    _description = 'Pelanggan'
    _inherits    = {'res.partner': 'partner_id'}

