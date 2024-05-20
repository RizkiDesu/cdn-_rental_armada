from odoo import models, fields, api, _




class ProductTemplate(models.Model):
    _inherit = 'product.template'

    nama_armada     = fields.Char(string='Nama Armada', required=True)
    
    jenis_armada    = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')])
    