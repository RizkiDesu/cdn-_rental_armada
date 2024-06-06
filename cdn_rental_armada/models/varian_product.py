from odoo import _, api, fields, models, tools

class ProductProduct(models.Model):
    _inherit            = 'product.product'
    jenis_armada        = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True, default='mobil')
    armada_id = fields.Integer(string='ID Armada')
    
    
    # @tools.ormcache()
    # def _set_default_uom_id(self):
    #     return self.env.ref('uom.product_uom_day')
    
    # @api.model
    # def default_get(self, fields):
    #     res = super(ProductProduct, self).default_get(fields)
    #     satuan = self._set_default_uom_id()
    #     if satuan:
    #         self.uom_id     = satuan.id
    #         self.uom_po_id  = satuan.id
            
    #     return res
    
