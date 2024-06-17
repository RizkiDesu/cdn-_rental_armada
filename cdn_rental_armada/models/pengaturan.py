from odoo import _, api, fields, models


# CREATED BY TRIADI
# UPDATE BY RIZKI
# ------------------------------- PENGATURAN --------------------------------
class ResConfigSetting(models.TransientModel):
    _inherit        = 'res.config.settings'
    
    # ------------------------------- JANGKA WAKTU WAJAR SERVICE --------------------------------
    jangka_waktu    = fields.Integer(string='Jangka Waktu', config_parameter="cdn_rental_armada.jangka_waktu", default=30)

    # ------------------------------- PENGATURAN WEBSITE HOME -----------------------------------
    slogan          = fields.Char(string='Slogan', config_parameter="cdn_rental_armada.slogan", default="Pilihan Tepat untuk Setiap Perjalanan.")
    deskripsi       = fields.Char(string='Deskripsi', config_parameter="cdn_rental_armada.deskripsi", default="deskripsi persewaan")
    deskripsi_id    = fields.Many2one(comodel_name='cdn.deskripsi', string='deskripsi layanan', config_parameter="cdn_rental_armada.deskripsi_id")
    
    
    headline        = fields.Char(string='Headline', config_parameter="cdn_rental_armada.headline", default="50%")
    deskripsi_event = fields.Char(string='Deskripsi Event', config_parameter="cdn_rental_armada.event", default="event persewaan")
    tanggal_event   = fields.Datetime(string='Tanggal Event', config_parameter="cdn_rental_armada.tanggal_event")

    # ------------------------------- URL API --------------------------------
    url_api         = fields.Char(string='URL API', config_parameter="cdn_rental_armada.url_api" , default="http://localhost:8069/virtual_account/create")




class CdnDeskripsi(models.Model):
    _name = 'cdn.deskripsi'
    _description = 'Cdn Deskripsi'

    name = fields.Char(string='Nama')
    # slogan = fields.Char(string='Slogan')
    deskripsi = fields.Text(string='Deskripsi')

class CdnYourService(models.Model):
    _name = 'cdn.your.service'
    _description = 'Your Service'
    
    name = fields.Char(string='Nama Layanan')
    deskripsi = fields.Text(string='Deskripsi Layanan')
    


    
    
    

    
 
