from odoo import _, api, fields, models
from datetime import date
from dateutil import relativedelta

#adi
class CdnArmada(models.Model):
    _name            = 'cdn.armada'
    _description     = 'Armada'
    _sql_constraints = [
        ('unique_no_plat', 'Unique(no_plat)','Nomor polisi tidak boleh sama!'),
        ('unique_no_mesin', 'Unique(no_mesin)','Nomor mesin tidak boleh sama!'),
    ]

    merek_id        = fields.Many2one(comodel_name='cdn.merek', string='Merek Kendaraan',required=True)
    jenis_kendaraan = fields.Many2one(comodel_name='cdn.jenis.kendaraan', string='Jenis Kendaraan',required=True, domain="[('merek_id', '=', merek_id)]")
    jumlah_kursi    = fields.Integer(string='Jumlah Kursi', required=True, default="2")
    jenis_armada    = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
    tahun_pembuatan = fields.Integer(string='Tahun Pembuatan', required=True, default=lambda self: date.today().year)
    no_plat         = fields.Char(string='Plat Nomor', required=True)
    no_mesin        = fields.Char(string='No Rangka & No Mesin',required=True)
    
    kondisi          = fields.Boolean(string='Kondisi Kendaraan', help="Jika aktif berarti armada dalam kondisi bagus", compute="_compute_kondisi")

    foto_mobil       = fields.Image('Foto Armada')
    service_ids      = fields.One2many(comodel_name='cdn.service', inverse_name='armada_id', string='List Armada')
    hitung_service   = fields.Integer(string='Jumlah Service', compute="_compute_service_count", store=True)
    terakhir_service = fields.Date(string='Terakhir Service', compute='_compute_tanggal_service_terakhir', store=True)
    state           = fields.Selection(string='Status Armada', selection=[('tidak_siap','Tidak Siap'), ('dipakai', 'Sedang Dipakai'), ('siap', 'Siap Dipakai')])

    @api.model
    def create(self, vals):
        # vals
        if 'jenis_kendaraan' in vals and isinstance(vals['jenis_kendaraan'], str):
            jenis_kendaraan_name = vals['jenis_kendaraan']
            merek_id             = vals.get('merek_id')
            jenis_kendaraan      = self.env['cdn.jenis.kendaraan'].create({
                'name': jenis_kendaraan_name,
                'merek_id': merek_id,
            })
            vals['jenis_kendaraan'] = jenis_kendaraan.id
        res = super(CdnArmada, self).create(vals)
        return res

    @api.onchange('kondisi')
    def _onchange_kondisi(self): # fix bug rizki
        if  self.kondisi == True:
            self.state = 'siap'
        if  self.kondisi == False:
            self.state = 'tidak_siap'
        if self.kondisi not in (False, True): # jika kondisi tidak diisi
            self.state = 'tidak_siap'
        # if self.terakhir_service is None : 
        #     self.state = 'service'

    @api.depends('service_ids.tanggal')
    def _compute_tanggal_service_terakhir(self):
        for rec in self:
            services = self.env['cdn.service'].search([('armada_id', '=', rec.id)], order='tanggal desc', limit=1)
            if services:
                rec.terakhir_service = services.tanggal
            else:
                rec.terakhir_service = rec.terakhir_service # fix bug rizki
    def name_get(self):
        return [(record.id, "[ %s ][ %s ] %s %s" % (record.jenis_armada, record.no_plat, record.merek_id.name, record.jenis_kendaraan.name)) for record in self]
    
    
    def tombol_service(self):
        return {
            'name': _('Perawatan Armada'),
            'res_model': 'cdn.service',
            'view_mode': 'list,form',
            'context': {'default_service_id':self.id},
            'domain': [('armada_id','=',self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }
    @api.depends('service_ids')
    def _compute_service_count(self):
        Jmlh = self.env['cdn.service']
        for rec in self:
            rec.hitung_service = Jmlh.sudo().search_count([('armada_id','=',rec.id)])
        
    def tombol_jenis(self):
        return {
            'name': _('Armada'),
            'res_model': 'cdn.armada',
            'view_mode': 'list,form,kanban',
            'context': {'default_jenis_armada':self.jenis_armada},
            'domain': [('jenis_armada','=',self.jenis_armada)],
            'type': 'ir.actions.act_window'
        }
        
    def tombol_merek_action(self):
        return {
            'name': _('Merek Kendaraan'),
            'res_model': 'cdn.merek',
            'view_mode': 'list,form',
            'type': 'ir.actions.act_window'
        }

    def action_state_siap(self) :
        for rec in self : 
            rec.state = 'siap'

    def action_state_dipakai(self) :
        for rec in self : 
            rec.state = 'dipakai'

    def action_state_tidak_siap(self) :
        for rec in self : 
            rec.state = 'tidak_siap'

    @api.depends('terakhir_service')
    def _compute_kondisi(self):
        # state 
        for rec in self: 
            is_keadaan = None
            hari_ini = date.today()
            jangka_waktu = self.env['ir.config_parameter'].get_param('cdn_rental_armada.jangka_waktu')
            hari_batal_wajar = hari_ini - relativedelta.relativedelta(days=int(jangka_waktu))
            if rec.terakhir_service : 
                if hari_batal_wajar < rec.terakhir_service:
                    is_keadaan = False
                else :
                    is_keadaan = True 
            rec.kondisi = is_keadaan