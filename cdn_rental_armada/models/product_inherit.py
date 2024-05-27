from odoo import models, fields, api, _




class ProductTemplate(models.Model):
    _inherit        = 'product.template'

    # nama_armada     = fields.Char(string='Nama Armada', required=True)
    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Nama Armada')
    jenis_armada    = fields.Selection(string='Jenis Armada', related='armada_id.jenis_armada', store=True)


    

    
    