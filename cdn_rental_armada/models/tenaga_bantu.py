from odoo import _, api, fields, models

class TenagaKerja(models.Model):
    _name = "cdn.tenaga.bantu"
    _description = "Tenaga Bantu"
    _inherits = {'res.partner': 'partner_id'}

   
    sim_ids      = fields.One2many(comodel_name='cdn.sim', inverse_name='sim_id', string='Izin Mengemudi')





