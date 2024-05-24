from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    jenis_armada     = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True, default='mobil')    
    
