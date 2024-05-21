from odoo import models, fields, api, _


class CdnProduk(models.Model):
    _name           = 'cdn.produk'
    _description    = 'Produk'
    _inherits       = {'product.template':'product_id'}
    
    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Nama Armada')
    jenis_armada    = fields.Selection(string='Jenis Armada', related='armada_id.jenis_armada')
    merek           = fields.Many2one(string='Merek', related='armada_id.merek_id')
    jenis_kendaraan = fields.Many2one(string='Jenis Kendaraan', related='armada_id.jenis_kendaraan')
    jumlah_kursi    = fields.Integer(string='Jumlah Kursi', related='armada_id.jumlah_kursi')
    tahun_pembuatan = fields.Integer(string='Tahun Pembuatan', related='armada_id.tahun_pembuatan')
    no_plat         = fields.Char(string='Plat Nomor', related='armada_id.no_plat')
    no_mesin        = fields.Char(string='No Rangka & No Mesin', related='armada_id.no_mesin')