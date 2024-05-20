from odoo import _, api, fields, models
from datetime import date


#adi
class CdnArmada(models.Model):
    _name            = 'cdn.armada'
    _description     = 'Armada'
    _sql_constraints = [
        ('unique_no_plat', 'Unique(no_plat)','Nomor polisi tidak boleh sama!'),
        ('unique_no_mesin', 'Unique(no_mesin)','Nomor mesin tidak boleh sama!'),
    ]

    merek_id        = fields.Many2one(comodel_name='cdn.merek', string='Merek Kendaraan',required=True)
    jenis_kendaraan = fields.Many2one(comodel_name='cdn.jenis.kendaraan', string='Jenis Kendaraan',required=True,domain="[('merek_id', '=', merek_id)]")
    jumlah_kursi    = fields.Integer(string='Jumlah Kursi', required=True, default="2")
    jenis_armada    = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
    tahun_pembuatan = fields.Integer(string='Tahun Pembuatan', required=True, default=lambda self: date.today().year)
    no_plat         = fields.Char(string='Plat Nomor', required=True)
    no_mesin        = fields.Char(string='No Rangka & No Mesin',required=True)
    kondisi         = fields.Boolean(string='Kondisi Armada', default="True", help="Jika aktif berarti armada dalam kondisi bagus")
    foto_mobil      = fields.Image('Foto Armada')
    
    def name_get(self):
        return [(record.id, "[ %s ] %s %s" % (record.jenis_armada, record.merek_id.name, record.jenis_kendaraan.name)) for record in self]
    
    @api.model
    def create(self, vals):
        if 'jenis_kendaraan' in vals and isinstance(vals['jenis_kendaraan'], str):
            jenis_kendaraan_name = vals['jenis_kendaraan']
            merek_id             = vals.get('merek_id')
            jenis_kendaraan      = self.env['cdn.jenis.kendaraan'].create({
                'name': jenis_kendaraan_name,
                'merek_id': merek_id,
            })
            vals['jenis_kendaraan'] = jenis_kendaraan.id
        return super(CdnArmada, self).create(vals)