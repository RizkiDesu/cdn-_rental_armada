from odoo import _, api, fields, models


# CREATED BY IAN
# REVISI BY ALVITO
# ------------------------------- TENAGA BANTU --------------------------------
class CdnTenagaKerja(models.Model):
    _name           = "cdn.tenaga.bantu"
    _description    = "Tenaga Bantu"
    _inherits       = {'res.partner': 'partner_id'}
    _inherit         = ['mail.thread', 'mail.activity.mixin']
    
    state           = fields.Selection(string='Status Tenaga Bantu', selection=[('tidak_aktif','Tidak Aktif'), ('perjalanan', 'Bertugas'), ('siap', 'Siap')], default='tidak_aktif')
    # sim_ids         = fields.One2many(comodel_name='cdn.sim', inverse_name='sim_id', string='Izin Mengemudi')
    
    def action_state_siap(self):
        for rec in self:
            rec.state   = 'siap'
            rec.status  = 'aktif'
        
    def action_state_perjalanan(self):
        for rec in self:
            rec.state   = 'perjalanan'
        
    def action_state_tidak_aktif(self):
        for rec in self:
            rec.state   = 'tidak_aktif'
            rec.status  = 'aktif'