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

    merek_id         = fields.Many2one(comodel_name='cdn.merek', string='Merek Kendaraan',required=True)
    jenis_kendaraan  = fields.Many2one(comodel_name='cdn.jenis.kendaraan', string='Jenis Kendaraan',required=True, domain="[('merek_id', '=', merek_id)]")
    jumlah_kursi     = fields.Integer(string='Jumlah Kursi', required=True, default="2")
    jenis_armada     = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], required=True)    
    tahun_pembuatan  = fields.Integer(string='Tahun Pembuatan', required=True, default=lambda self: date.today().year)
    no_plat          = fields.Char(string='Plat Nomor', required=True)
    no_mesin         = fields.Char(string='No Mesin',required=True)
    no_rangka        = fields.Char(string='No Rangka',required=True)
    history_ids      = fields.One2many(comodel_name='cdn.history', inverse_name='armada_id', string='List Armada')
    
           
    kondisi          = fields.Boolean(string='Kondisi Kendaraan', help="Jika aktif berarti armada dalam kondisi bagus", compute="_compute_kondisi")

    foto_mobil       = fields.Image('Foto Armada')
    service_ids      = fields.One2many(comodel_name='cdn.service', inverse_name='armada_id', string='List Armada')
    ujikir_ids       = fields.One2many(comodel_name='cdn.uji.kir', inverse_name='armada_id', string='List Uji Kir')
    hitung_service   = fields.Integer(string='Jumlah Service', compute="_compute_service_count", store=True)
    berlaku_ujikir   = fields.Date(string='Berlaku Uji Kir', compute='_compute_tanggal_ujikir_terakhir', store=True)
    terakhir_service = fields.Date(string='Terakhir Service', compute='_compute_tanggal_service_terakhir', store=True)
    tanggal_pakai    = fields.Date(string='Terakhir di pakai', compute = '_compute_tanggal_pakai', store = True)   
    state            = fields.Selection(string='Status Armada', selection=[('tidak_siap','Tidak Siap'), ('dipakai', 'Sedang Dipakai'), ('siap', 'Siap Dipakai')])

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
    @api.depends('ujikir_ids.tanggal_berakhir')
    def _compute_tanggal_ujikir_terakhir(self):
        for rec in self:
            ujikir = self.env['cdn.uji.kir'].search([('armada_id', '=', rec.id)], order='tanggal_berakhir desc', limit=1)
            if ujikir:
                rec.berlaku_ujikir = ujikir.tanggal_berakhir
            else:
                rec.berlaku_ujikir = None

    @api.depends('service_ids.tanggal')
    def _compute_tanggal_service_terakhir(self):
        for rec in self:
            services = self.env['cdn.service'].search([('armada_id', '=', rec.id)], order='tanggal desc', limit=1)
            if services:
                rec.terakhir_service = services.tanggal
            else:
                rec.terakhir_service = None # fix bug rizki
    #Alvito
    @api.depends('history_ids.tgl_pakai')
    def _compute_tanggal_pakai(self):
        for rec in self:
            history = self.env['cdn.history'].search([('armada_id', '=', rec.id)], order='tgl_pakai desc', limit=1)
            if history:
                rec.tanggal_pakai = history.tgl_pakai
            else:
                rec.tanggal_pakai = None

    def name_get(self):
        return [(record.id, "[ %s ][ %s ] %s %s" % (record.jenis_armada, record.no_plat, record.merek_id.name, record.jenis_kendaraan.name)) for record in self]
    
    # rizki
    def tombol_ujikir(self):
        action = self.env["ir.actions.actions"]._for_xml_id("cdn_rental_armada.cdn_uji_kir_action")
        action['domain'] = [('armada_id', '=', self.id)]
        action['context'] = {'default_armada_id': self.id}
        return action
    
    #Alvito
    def tombol_history(self):
        return {
            'name': _('History Perjalanan'),
            'res_model': 'cdn.history',
            'view_mode': 'list,form',
            'context': {'default_history_id':self.id},
            'domain': [('armada_id','=',self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }
    
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