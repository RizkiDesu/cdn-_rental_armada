from odoo import models, fields, api, _


class CdnSaleOrder(models.Model):
   _inherit = 'sale.order'

   jenis_armada   = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
   invoice_id     = fields.Many2one('account.move', copy=False,string='Invoice',help='Invoice Patient')
   
   @api.onchange('jenis_armada')
   def _onchange_jenis_armada(self):
      if self.jenis_armada:
         self.order_line = [(5, 0, 0)]
         
   def aksi_invoice(self):
      """Method for creating invoice"""
      self.state = 'sale'
      self.invoice_id = self.env['account.move'].sudo().create({
         'move_type': 'out_invoice',
         'date': fields.Date.today(),
         'invoice_date': fields.Date.today(),
         'partner_id': self.partner_id.id,
         'invoice_line_ids': [(0, 0, {
                'product_id': self.env.ref("product.product").id,
                'quantity': self.env.ref("product.product").product.uom.qty,
                'price_unit': self.env.ref("product.product").price_unit,
            })],
      })
         
class CdnSaleOrderLines(models.Model):
   _inherit = 'sale.order.line'
   
   armada_id      = fields.Many2one(comodel_name='cdn.armada', string='Armada')
   supir          = fields.Many2one(comodel_name='cdn.supir', string='Supir')
   tenaga_bantu   = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantu')
   


