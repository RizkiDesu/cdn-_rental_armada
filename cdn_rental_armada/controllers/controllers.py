# -*- coding: utf-8 -*-
from odoo import http
import traceback
from odoo.http import Response, request
from odoo.loglevels import ustr
import sys
import json
from datetime import date


# http://localhost:8069/pembayaran/invoice
class pembayaran(http.Controller):
   @http.route('/pembayaran/invoice', type='http', auth='public', website=False, methods=['POST', 'GET'], csrf=False, cors='*')
   def tes(self, **kwargs):
      try:
         i_param   = request.get_json_data()
         i_va      = i_param['virtual_account']
         i_amount  = i_param['amount']
         i_date    = i_param['date']
         i_kp      = i_param['kode_pengesahan']
         datarow             = {
            'is_success'    : True,
            'code'          : 200,
            'va'            : i_va,
            'amount'        : i_amount,
            'date'          : i_date,
            'kode_p'        : i_kp,
         }
         print(datarow)


         # invoices = http.request.env['account.move'].search([('name', '=', datarow['va'])])
         # if not invoices:
         #    raise UserError("Invoice with name {} not found.".format(datarow['va']))
         # wizard = http.request.env['account.payment.register'].create({
         #    'payment_date' : datarow['date'],
         #    'amount'       : datarow['amount'],
         #    'payment_method_id' : 1,
         #    'journal_id'   : 1,
         #    'communication' : datarow['kode_p'],
         #    'partner_id'   : 1,
         #    'partner_type' : 'customer',
         #    'payment_type' : 'inbound',
         #    'payment_difference_handling' : 'open',
         #    'currency_id'  : 1,
         #    'payment_method_id' : 1,
         # })
         # # wizard.invoice_ids = [(6, 0, invoices.ids)]
         # wizard.action_create_payments()
         

         invoice_id = request.env['account.move'].sudo().search([('name', '=', datarow['va'])])


         print(invoice_id.name)
         print(invoice_id.partner_id.name)
         print(invoice_id.amount_total)
         # payment.action_post()
         payment = request.env['account.payment'].sudo().create({
               # 'payment_type': 'outbound',  # or 'inbound'
               # 'partner_type': 'supplier',  # or 'customer'
               'partner_id': invoice_id.partner_id.id,  # ID of the partner
               'amount': datarow['amount'],
               'date': datarow['date'],
               # 'journal_id': 1,  # ID of the payment journal
               # 'payment_method_id': 1,  # ID of the payment method
            })
         payment.action_post()
        
         
         # action_data = invoice.action_register_payment()
         # invoice.payment_by_id = action_data['context']['default_journal_id'] = request.env.user.company_id.account_journal_id.id
         # wizard = Form(request.env['account.payment.register'].with_context(action_data['context'])).save()
         # action = wizard.action_create_payments()
         # # invoice.write({'payment_state': 'paid'})
         # success_invoice_payment.append(invoice)

      except Exception as e:
         traceback.print_exception(*sys.exc_info()) 
         datarow['is_success']   = ustr(e)
         datarow['code']         = 201
      finally:
         body = json.dumps(datarow)
         return Response(
               body, 
               status  = 200, 
               headers = [
                  ('Content-Type', 'application/json'), 
                  ('Content-Length', len(body))
               ]
         )
# class CdnRentalArmada(http.Controller):
#     @http.route('/cdn_rental_armada/cdn_rental_armada', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cdn_rental_armada/cdn_rental_armada/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cdn_rental_armada.listing', {
#             'root': '/cdn_rental_armada/cdn_rental_armada',
#             'objects': http.request.env['cdn_rental_armada.cdn_rental_armada'].search([]),
#         })

#     @http.route('/cdn_rental_armada/cdn_rental_armada/objects/<model("cdn_rental_armada.cdn_rental_armada"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cdn_rental_armada.object', {
#             'object': obj
#         })
