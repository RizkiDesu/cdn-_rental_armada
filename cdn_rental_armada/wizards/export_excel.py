from odoo import _, api, fields, models
import time
import requests
import json
import random
import string

class WizardArmadaTersedia(models.TransientModel):
    _name = 'wizard.armada.tersedia'
    _description = 'Wizard Armada Tersedia'
    
    jenis_armada = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'), ('mobil', 'Mobil')], tracking=True)    
    state = fields.Selection(string='Status Armada', selection=[('tidak_siap', 'Tidak Siap'), ('dipakai', 'Sedang Dipakai'), ('siap', 'Siap Dipakai')])
    
    def export_excel(self):
      source_data = {
         "virtual_account" : ''.join(random.choices(string.digits, k=10)),
         "amount" : "900000",
         "exp_date" : "2024-07-12",
         "description" : "awokaowdkoa"
      }
      # headers = {'Content-Type': 'application/json'}
      response = requests.post('{}/virtual_account/create'.format('http://localhost:8069'), headers={'Content-Type': 'application/json'}, data=json.dumps(source_data))
      print(response)
      print(response.json()['is_success'])

      pass
      # return {
      #    'type': 'ir.actions.client',
      #    'tag': 'display_notification',
      #    'params': {
      #       'title': 'Berhasil',
      #       'type': 'success',
      #       'message': 'Armada telah kembali',
      #       'sticky': False,
      #       'next' : {
      #             'type' : 'ir.actions.act_window_close'
      #       }
      #    }
      # }
