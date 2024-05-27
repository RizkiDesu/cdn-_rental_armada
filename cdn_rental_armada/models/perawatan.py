from odoo import _, api, fields, models
from datetime import date
from dateutil import relativedelta
import logging

_logger = logging.getLogger(__name__)

# Triadi
class CdnService(models.Model):
    _name           = 'cdn.service'
    _description    = 'Service'
    _rec_name       = 'tanggal'
    
    
    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Armada', required=True)
    tanggal         = fields.Date(string='Tanggal service')
    jenis_service   = fields.Char(string='Jenis Perawatan')
    harga           = fields.Integer(string='Pengeluran')
    deskripsi       = fields.Text(string='Deskripsi')
    

    @api.model
    def create(self, vals):
        record      = super(CdnService, self).create(vals)
        hari_ini    = date.today()
        if 'tanggal' in vals:    
            jangka_waktu = self.env['ir.config_parameter'].get_param('cdn_rental_armada.jangka_waktu')
            hari_batal_wajar = hari_ini - relativedelta.relativedelta(days=int(jangka_waktu))
            tgl     = fields.Date.from_string(vals['tanggal'])
            cek     = self.env['cdn.armada'].search([('id', '=', record.armada_id.id)])
            if hari_batal_wajar < tgl:
                cek.state       = 'siap'
                cek.kondisi     = True
            else :
                cek.state       = 'tidak_siap'
                cek.kondisi     = False
        return record

class CdnUjiKir(models.Model):
    _name           = 'cdn.uji.kir'
    _description    = 'Cdn Uji Kir'
    _rec_name       = 'tanggal_berakhir'

    armada_id       = fields.Many2one(comodel_name='cdn.armada', string='Armada', required=True)
    tanggal         = fields.Date(string='Tanggal Uji Kir')
    tanggal_berakhir = fields.Date(string='Berlaku Sampai')
    deskripsi       = fields.Text(string='Deskripsi')
    foto_uji        = fields.Image('Foto Uji Kir')


