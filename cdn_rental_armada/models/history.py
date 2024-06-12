from odoo import _, api, fields, models

# CREATED BY ALVITO
# ------------------------------- HISTORY --------------------------------
class CdnHistory(models.Model):
    _name           = 'cdn.history'
    _description    = 'Rangka & Mesin'
    _rec_name       = 'tujuan'
    _inherit     = ['mail.thread', 'mail.activity.mixin']

    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Armada')
    jarak           = fields.Integer(string='Jarak (km)')
    km_akhir        = fields.Float(string='Kilometer Terakhir (km)')
    tgl_pakai       = fields.Date(string='Tanggal Dipakai')
    tujuan          = fields.Char(string='Tujuan')
    hari            = fields.Integer(string='Di Pakai Berapa Hari')

    
    
    
    
   
    
    