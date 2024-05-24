from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    jenis_armada     = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True, default='mobil')   
    
    @api.model
    def create(self, vals):
        satuan = self.env['uom.uom'].search([('name', '=', 'Hari')], limit=1)
        if satuan:
            vals['uom_id'] = satuan.id
            vals['uom_po_id'] = satuan.id
            print('pruint..............................................')
            print(satuan.id)
        return super(ProductProduct, self).create(vals) 
    
