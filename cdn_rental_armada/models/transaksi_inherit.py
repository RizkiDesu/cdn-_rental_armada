from odoo import models, fields, api, _


class CdnSaleOrder(models.Model):
   _inherit = 'sale.order'

   jenis_armada   = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
   
   @api.onchange('jenis_armada')
   def _onchange_jenis_armada(self):
      if self.jenis_armada:
         self.order_line = [(5, 0, 0)]
         
class CdnSaleOrderLines(models.Model):
   _inherit = 'sale.order.line'
   
   supir          = fields.Many2one(comodel_name='cdn.supir', string='Supir')
   tenaga_bantu   = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantu')


