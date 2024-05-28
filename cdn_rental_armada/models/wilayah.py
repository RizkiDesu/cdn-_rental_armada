from odoo import models, fields, api
# adi
class cdnPropinsi(models.Model):
    _name = 'cdn.propinsi'
    _description = 'Propinsi'
    
    name = fields.Char(string='Nama Propinsi', required=True)
    kode = fields.Char(string='Kode Propinsi')
    singkat = fields.Char(string='Singkatan')
    keterangan = fields.Text(string='keterangan')
    kota_ids = fields.One2many(comodel_name='cdn.kota', inverse_name='propinsi_id', string='Daftar List Kota')
    

class cdnKota(models.Model):
    _name = 'cdn.kota'
    _description = 'Kota'
    
    name = fields.Char(string='Nama Kota', required=True)
    kode = fields.Char(string='Kode Kota')
    propinsi_id = fields.Many2one(comodel_name='cdn.propinsi', string='Nama Propinsi')
    
    singkat = fields.Char(string='Singkatan')
    keterangan = fields.Text(string='keterangan')
    kecamatan_ids = fields.One2many(comodel_name='cdn.kecamatan', inverse_name='kota_id', string='Daftar kecamatan')
    


class cdnKecamatan(models.Model):
    _name = 'cdn.kecamatan'
    _description = 'cdn Kecamatan'
    
    name = fields.Char(string='Nama Kecamatan', required=True)
    kode = fields.Char(string='Kode Kecamatan')
    
    kota_id = fields.Many2one(comodel_name='cdn.kota', string='Nama Kota')
    keterangan = fields.Text(string='Keterangan')
    
    desa_ids = fields.One2many(comodel_name='cdn.desa', inverse_name='kecamatan_id', string='Daftar Desa')
    
    


class cdnDesa(models.Model):
    _name = 'cdn.desa'
    _description = 'cdn Desa'
    
    name = fields.Char(string='Nama Desa', required=True)
    kode = fields.Char(string='Kode Desa')
    keterangan = fields.Text(string='Keterangan')
    kecamatan_id = fields.Many2one(comodel_name='cdn.kecamatan', string='Nama Kecamatan')
    
    
    
    

    
    

    
    
    
    
    
    
    
    
