from odoo import models, fields, api, _


# CREATED BY IAN
# REVISI BY RIZKI
# ------------------------------- SUPRIR --------------------------------
class CdnSupir(models.Model):
    _name           = 'cdn.supir'
    _description    = 'Cdn Supir'
    _inherits       = {'res.partner' : 'partner_id'}
    _inherit        = ['mail.thread', 'mail.activity.mixin']
  
    # ------------------------------- FIELD --------------------------------
    state           = fields.Selection(string='Status Tenaga Bantu', selection=[('tidak_aktif','Tidak Aktif'), ('perjalanan', 'Bertugas'), ('siap', 'Siap')], default='tidak_aktif')
    
    # ------------------------------- RELATION --------------------------------
    sim_ids         = fields.One2many(comodel_name='cdn.sim', inverse_name='sim_id', string='Izin Mengemudi')
    
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

    @api.depends('status')
    def _compute_field_name(self):
        for rec in self:
            if rec.status == 'aktif':
                rec.state = 'siap'
            else:
                rec.state = 'tidak_aktif'
    
# CREATED BY IAN
# ------------------------------- SIM --------------------------------
class CdnSim(models.Model):
    _name         = 'cdn.sim'
    _description  = 'cdn.sim'
    _rec_name     = 'no_sim'
    _inherit        = ['mail.thread', 'mail.activity.mixin']

    # ------------------------------- RELATION --------------------------------
    sim_id      = fields.Many2one(comodel_name='cdn.supir', string='SUPIR', tracking=True)

    # ------------------------------- FIELD --------------------------------
    name        = fields.Char(string='Nama')
    no_sim      = fields.Char(string='No Sim', required=True, tracking=True)
    jenis_sim   = fields.Selection(string='Jenis Sim', selection=[('a', 'Sim A'), ('b', 'Sim B')], required=True, tracking=True) 
    foto_sim    = fields.Image('Foto Sim', required=True, tracking=True)
    masaberlaku = fields.Date(string='Masa Berlaku', tracking=True)
   
   