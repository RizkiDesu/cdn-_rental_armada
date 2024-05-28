from odoo import _, api, fields, models

#Alvito
class CdnHistory(models.Model):
    _name           = 'cdn.history'
    _description    = 'Rangka & Mesin'
    _rec_name       = 'tujuan'
    _inherit     = ['mail.thread', 'mail.activity.mixin']

    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Armada', required=True, tracking=True)
    jarak           = fields.Integer(string='Jarak (km)', tracking=True)
    tgl_pakai       = fields.Date(string='Tanggal Dipakai', required=True, tracking=True)
    tujuan          = fields.Char(string='Tujuan', required=True, tracking=True)
    hari            = fields.Integer(string='Di Pakai Berapa Hari', required=True, tracking=True)
    
    
    
    
   
    
    