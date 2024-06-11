from odoo import _, api, fields, models
import time

class WizardArmadaTersedia(models.TransientModel):
    _name = 'wizard.armada.tersedia'
    _description = 'Wizard Armada Tersedia'
    
    jenis_armada     = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], tracking=True)    
    state            = fields.Selection(string='Status Armada', selection=[('tidak_siap','Tidak Siap'), ('dipakai', 'Sedang Dipakai'), ('siap', 'Siap Dipakai')])
    

    def export_excel(self):
       return {
         'type': 'ir.actions.client',
         'tag': 'display_notification',
         'params': {
            'title': 'Berhasil',
            'type': 'success',
            'message': 'Armada telah kembali',
            'sticky': False,
            'next' : {
                'type' : 'ir.actions.act_window_close'
            }
         }
      }