from odoo import _, api, fields, models



class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    type_orang = fields.Selection(string='Tipe', selection=[('pelanggan', 'Pelanggan'), ('sopir', 'Sopir'),('tenaga_bantu', 'Tenaga bantu')],default="pelanggan")
    
