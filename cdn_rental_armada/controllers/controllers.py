# -*- coding: utf-8 -*-
from odoo import http
import traceback
from odoo.http import Response, request
from odoo.loglevels import ustr
import sys
import json

class pembayaran(http.Controller):
   @http.route('/pembayaran/tes', type='http', auth='public', website=False, methods=['POST', 'GET'], csrf=False, cors='*')
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
