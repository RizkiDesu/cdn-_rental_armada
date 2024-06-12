from odoo import _, api, fields, models


# Triadi
class ResConfigSetting(models.TransientModel):
    _inherit        = 'res.config.settings'
    
    jangka_waktu    = fields.Integer(string='Jangka Waktu', config_parameter="cdn_rental_armada.jangka_waktu", default=30)
    slogan          = fields.Char(string='Slogan', config_parameter="cdn_rental_armada.slogan", default="Pilihan Tepat untuk Setiap Perjalanan.")
    deskripsi       = fields.Char(string='Deskripsi', config_parameter="cdn_rental_armada.deskripsi", default="deskripsi persewaan")
    headline        = fields.Char(string='Headline', config_parameter="cdn_rental_armada.headline", default="50%")
    deskripsi_event = fields.Char(string='Deskripsi Event', config_parameter="cdn_rental_armada.event", default="event persewaan")
    tanggal_event   = fields.Datetime(string='Tanggal Event', config_parameter="cdn_rental_armada.tanggal_event")
    # pelayanan       = fields.Many2many(comodel_name='cdn.your.service', string='pelayanan', config_parameter="cdn_rental_armada.pelayanan")
    url_api         = fields.Char(string='URL API', config_parameter="cdn_rental_armada.url_api" , default="http://localhost:8069/virtual_account/create")


class CdnYourService(models.Model):
    _name = 'cdn.your.service'
    _description = 'Your Service'
    
    name = fields.Char(string='Nama Layanan')
    
    

    
    
    

    
 
