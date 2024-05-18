from odoo import _, api, fields, models


#adi
class CdnArmada(models.Model):
    _name = 'cdn.armada'
    _description = 'Cdn Armada'

    merek_id = fields.Many2one(comodel_name='cdn.merek', string='merek kendaraan',required=True)
    jenis_kendaraan = fields.Many2one(comodel_name='cdn.jenis.kendaraan', string='Jenis kendaraan',required=True)
    jumlah_kursi = fields.Integer(string='Jumlah Kursi', required=True)
    jenis_armada = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
    tahun_pembuatan = fields.Date(string='Tahun Pembuatan', required=True)
    no_plat = fields.Char(string='Plat Nomor', required=True)
    no_mesin = fields.Char(string='No Rangka & No Mesin',required=True)
    kondisi = fields.Boolean(string='Kondisi Armada', default="True")
    
    def name_get(self):
        return [(record.id, "[%s] : %s" % (record.jenis_armada, record.merek_id)) for record in self]
    
    
    
    