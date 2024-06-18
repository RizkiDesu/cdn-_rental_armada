from odoo import models, fields, api

# CREATED BY TRIADI
# ------------------------------- PROVINSI --------------------------------
class cdnPropinsi(models.Model):
    _name = 'cdn.propinsi'
    _description = 'Propinsi'
    
    name = fields.Char(string='Nama Propinsi')
    kode = fields.Char(string='Kode Propinsi')
    singkat = fields.Char(string='Singkatan')
    keterangan = fields.Text(string='keterangan')

    # ------------------------------- RELATIONSHIP --------------------------------
    kota_ids = fields.One2many(comodel_name='cdn.kota', inverse_name='propinsi_id', string='Daftar List Kota')
    
# ------------------------------- KOTA --------------------------------
class cdnKota(models.Model):
    _name = 'cdn.kota'
    _description = 'Kota'
    
    name = fields.Char(string='Nama Kota')
    kode = fields.Char(string='Kode Kota')
    singkat = fields.Char(string='Singkatan')
    keterangan = fields.Text(string='keterangan')

    # ------------------------------- RELATIONSHIP --------------------------------
    propinsi_id = fields.Many2one(comodel_name='cdn.propinsi', string='Nama Propinsi')
    kecamatan_ids = fields.One2many(comodel_name='cdn.kecamatan', inverse_name='kota_id', string='Daftar kecamatan')
    
# ------------------------------- KECAMATAN --------------------------------
class cdnKecamatan(models.Model):
    _name = 'cdn.kecamatan'
    _description = 'cdn Kecamatan'
    
    name = fields.Char(string='Nama Kecamatan')
    kode = fields.Char(string='Kode Kecamatan')
    keterangan = fields.Text(string='Keterangan')
    
    # ------------------------------- RELATIONSHIP --------------------------------
    kota_id = fields.Many2one(comodel_name='cdn.kota', string='Nama Kota')
    desa_ids = fields.One2many(comodel_name='cdn.desa', inverse_name='kecamatan_id', string='Daftar Desa')

# ------------------------------- DESA --------------------------------
class cdnDesa(models.Model):
    _name = 'cdn.desa'
    _description = 'cdn Desa'
    
    name = fields.Char(string='Nama Desa')
    kode = fields.Char(string='Kode Desa')
    keterangan = fields.Text(string='Keterangan')

    # ------------------------------- RELATIONSHIP --------------------------------
    kecamatan_id = fields.Many2one(comodel_name='cdn.kecamatan', string='Nama Kecamatan')
    
    
    
    

    
    

    
    
    
    
    
    
    
    
