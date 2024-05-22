from odoo import models, fields, api, _



# rizki (revisi)
class CdnSupir(models.Model):
    _name           = 'cdn.supir'
    _description    = 'Cdn Supir'
    _inherits       = {'res.partner' : 'partner_id'}

    
    sim_ids       = fields.One2many(comodel_name='cdn.sim', inverse_name='sim_id', string='Izin Mengemudi')
   
   
class CdnSim(models.Model):
   _name         = 'cdn.sim'
   _description  = 'cdn.sim'
   _rec_name     = 'no_sim'

   sim_id      = fields.Many2one(comodel_name='cdn.supir', string='SUPIR')
   name        = fields.Char(string='Nama')
   no_sim      = fields.Char(string='No Sim', required=True)
   jenis_sim   = fields.Selection(string='Jenis Sim', selection=[('a', 'Sim A'), ('b', 'Sim B')], required=True) 
   foto_sim    = fields.Image('Foto Sim', required=True)
   masaberlaku = fields.Date(string='Masa Berlaku')
   
   