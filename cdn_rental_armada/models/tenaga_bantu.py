from odoo import _, api, fields, models

class TenagaKerja(models.Model):
    _name = "cdn.tenaga.bantu"
    _description = "Tenaga Bantu"
    _inherits = {'res.partner': 'partner_id'}

    partner_id    = fields.Many2one(comodel_name='res.partner', string='Partner', required=True, ondelete='cascade')
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[('l', 'Laki Laki'), ('p', 'Perempuan')], required=True)
    no_ktp        = fields.Char(string='No KTP', required=True)
    umur          = fields.Integer(string='Umur', required=True)
    is_menikah    = fields.Boolean(string='Menikah', default=False, required=True)
    status        = fields.Selection(string='Status', selection=[('aktif', 'Aktif'), ('nonaktif', 'Nonaktif'),], default="aktif", required=True)
    sim_line      = fields.One2many(comodel_name='cdn.sim', inverse_name='sim_id', string='Izin Mengemudi')


class CdnSim(models.Model):
    _name         = 'cdn.sim'
    _description  = 'cdn.sim'

    sim_id      = fields.Many2one(comodel_name='res.partner', string='Partner')
    name        = fields.Char(string='Nama', required=True)
    no_sim      = fields.Char(string='No Sim', required=True)
    jenis_sim   = fields.Selection(string='Jenis Sim', selection=[('a', 'Sim A'), ('b', 'Sim B')], required=True) 
    foto_sim    = fields.Image('Foto Sim', max_width=60, required=True)


