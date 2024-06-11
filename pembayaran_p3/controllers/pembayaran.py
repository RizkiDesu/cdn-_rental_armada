# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import Response, request
from odoo.loglevels import ustr

import datetime
import traceback
import sys
import json

class pembayaran(http.Controller):
    @http.route('/virtual_account/create', type='http', auth='public', website=False, methods=['POST'], csrf=False, cors='*')
    def create(self, **kwargs):
        datarow             = {
            'is_success'    : True,
            'code'          : 200,
        }

        try:
            i_param         = request.get_json_data()
            i_va            = i_param['virtual_account']
            i_amount        = i_param['amount']
            i_exp_date      = i_param['exp_date']
            i_desc          = i_param['description']

            if not i_param:
                raise Exception('Parameter "param" tidak ditemukan')

            if not i_amount:
                raise Exception('Parameter "amount" tidak ditemukan')

            if not i_exp_date:
                raise Exception('Parameter "exp_date" tidak ditemukan')

            try:
                i_exp_date  = datetime.date.fromisoformat(i_exp_date)
            except:
                raise Exception('Format Tanggal Tidak Sesuai yyyy-mm-dd')

            record          = request.env['pembayaran_p3.pembayaran'].sudo().search([
                ('virtual_account', '=', i_va)
            ], limit=1)

            if record:
                raise Exception('Virtual Account Telah Terdaftar Sebelumnya')

            request.env['pembayaran_p3.pembayaran'].sudo().create({
                'virtual_account'   : i_va,
                'amount'            : i_amount,
                'exp_date'          : i_exp_date,
                'description'       : i_desc
            })
        except Exception as e:
            traceback.print_exception(*sys.exc_info()) 
            datarow['is_success']   = ustr(e)
            datarow['code']         = 201
        finally:
            body                    = json.dumps(datarow)
            return Response(
                body, 
                status  = 200, 
                headers = [
                    ('Content-Type', 'application/json'), 
                    ('Content-Length', len(body))
                ]
            )