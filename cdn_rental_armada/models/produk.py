from odoo import _, api, fields, models, tools

# CREATED BY TRIADI
# ------------------------------- INHERIT PRODUCT PRODUCT --------------------------------
class ProductProduct(models.Model):
    _inherit            = 'product.product'
    
    jenis_armada        = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')])
    armada_id           = fields.Integer(string='ID Armada')


# CREATED BY TRIADI
# REVISI BY RIZKI
# ------------------------------- PRODUK ARMADA AUTO CREATE PRODUCT VARIANT --------------------------------
class CdnProdukArmada(models.Model):
    _name = 'cdn.produk.armada'
    _description = 'Cdn Produk Armada'
    _inherit        = ['mail.thread', 'mail.activity.mixin']

    @tools.ormcache()
    def _get_default_uom_id(self):
        """Method for getting the default uom id"""
        return self.env.ref('uom.product_uom_day')
    
    # ------------------------------- PRODUK --------------------------------
    name = fields.Char(string='Nama Produk', tracking=True) 
    lst_price = fields.Float(string='Harga', tracking=True)
    taxes_id = fields.Many2many(comodel_name='account.tax', string='Pajak', tracking=True)
    images = fields.Image('image', tracking=True)
    description = fields.Text(string='Deskripsi', tracking=True)
    jenis_armada = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], tracking=True)
    uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure',
                            default=_get_default_uom_id, required=True,
                            help="Default unit of measure used for all stock operations.", tracking=True)

    # CREATED BY TRIADI
    # ------------------------------- PRIORITASKAN PRODUK --------------------------------
    priority = fields.Selection([
                        ('0', 'Normal'),
                        ('1', 'Favorite'),
                    ], default='0', string="Favorite", tracking=True)
                    
    # CREATED BY RIZKI
    # ------------------------------- AUTO CREATE PRODUCT --------------------------------
    @api.model
    def create(self, vals):
        produk_baru = super(CdnProdukArmada, self).create(vals)
        produk = self.env['product.product']
        produk.create({
            'name': produk_baru.name,
            'lst_price': produk_baru.lst_price,
            'taxes_id': [(6, 0, produk_baru.taxes_id.ids)],
            'image_1920': produk_baru.images,
            'description_sale': produk_baru.description,
            'jenis_armada': produk_baru.jenis_armada,
            'uom_id': produk_baru.uom_id.id,
            'uom_po_id': produk_baru.uom_id.id,
            'armada_id': produk_baru.id,
            'priority' : produk_baru.priority
        })
        return produk_baru

    # ------------------------------- UPDATE PRODUCT --------------------------------
    def write(self, vals):
        update = super(CdnProdukArmada, self).write(vals)
        produk = self.env['product.product'].search([('armada_id', '=', self.id)])
        produk.write({
            'name': self.name,
            'lst_price': self.lst_price,
            'taxes_id': [(6, 0, self.taxes_id.ids)],
            'image_1920': self.images,
            'description_sale': self.description,
            'jenis_armada': self.jenis_armada,
            'uom_id': self.uom_id.id,
            'uom_po_id': self.uom_id.id,
            'priority' : self.priority
        })
        return update

    # ------------------------------- DELETE PRODUCT --------------------------------
    def unlink(self):
        self.env['product.product'].search([('armada_id', '=', self.id)]).unlink()
        return super(CdnProdukArmada, self).unlink()
