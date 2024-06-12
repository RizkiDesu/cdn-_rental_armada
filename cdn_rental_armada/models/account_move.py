from odoo import _, api, fields, models
import requests
import json
from datetime import date


# CREATED BY IAN
# ------------------------------ INVOICE ---------------------------------------------
class AccountMove(models.Model):
    _inherit = 'account.move' 
    pemesanan_id   = fields.Integer(string='ID Pemesanan')
    tagihan_denda  = fields.Boolean(string='Tagihan Denda', default=False)

    # CREATED BY RIZKI
    # ------------------------------ KIRIM KE API PEMBAYARAN ---------------------------------------------
    def action_post(self):
        moves_with_payments = self.filtered('payment_id')
        other_moves = self - moves_with_payments
        if moves_with_payments:
            moves_with_payments.payment_id.action_post()
        if other_moves:
            other_moves._post(soft=False)
        url = self.env['ir.config_parameter'].get_param('cdn_rental_armada.url_api')
        data_bayar = {
            "virtual_account" : self.name,
            "amount" : self.amount_total,
            "exp_date" : fields.Date.to_string(self.invoice_date_due),
            "description" : "Pembayaran Invoice",
        }
        print(data_bayar)
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data_bayar))
        return False  
        
# CREATED BY IAN
# ------------------------------ INVOICE LINE ---------------------------------------------
class AccountMove(models.Model):
    _inherit = 'account.move.line'
    
    produk_pemesanan_id  = fields.Many2one('cdn.pemesanan.armada', string='Produk Armada')

    # ------------------------------ TAMBAHAN LINE ---------------------------------------------
    supir                = fields.Many2one(comodel_name='cdn.supir', string='Supir')
    tenaga_bantu         = fields.Many2one(comodel_name='cdn.tenaga.bantu', string='Tenaga Bantu')
    armada_id            = fields.Many2one(comodel_name='cdn.armada', string='Armada')
    jenis_armada         = fields.Selection(related='armada_id.jenis_armada')    
    
    
    
