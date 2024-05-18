from odoo import _, api, fields, models

class CdnjenisKendaraan(models.Model):
    _name = 'cdn.jenis.kendaraan'
    _description = 'cdn jenis kendaraan'

    name = fields.Char(string='Jenis Kendaraan', required=True)
    merek_id = fields.Many2one(comodel_name='cdn.merek', string='Merek')

