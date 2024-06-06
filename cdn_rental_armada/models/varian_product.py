from odoo import _, api, fields, models

class ProductProduct(models.Model):
    _inherit            = 'product.product'
    jenis_armada        = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True, default='mobil')   
    @api.model
    def default_get(self, fields):
        res = super(ProductProduct, self).default_get(fields)
        satuan = self.env['uom.uom'].search([('name', '=', 'Hari')], limit=1)
        if satuan:
            self.uom_id     = satuan.id
            self.uom_po_id  = satuan.id

        return res
    
