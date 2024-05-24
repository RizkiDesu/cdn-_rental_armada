from odoo import _, api, fields, models


class CdnRangkaMesin(models.Model):
    _name = 'cdn.rangka.mesin'
    _description = 'Rangka & Mesin'
    

   
    jenis = fields.Selection(string='Jenis', selection=[('rangka', 'Rangka'), ('mesin', 'Mesin'),])
    no = fields.Char(string='No')
    
    