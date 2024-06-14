from odoo import _, api, fields, models
from datetime import date
from dateutil import relativedelta

# CREATED TRIADI
# ------------------------------- ARMADA --------------------------------
class CdnArmada(models.Model):
    _name            = 'cdn.armada'
    _description     = 'Armada'
    _inherit         = ['mail.thread', 'mail.activity.mixin']


    _sql_constraints = [
        ('unique_no_plat', 'Unique(no_plat)','Nomor polisi tidak boleh sama!'),
        ('unique_no_mesin', 'Unique(no_mesin)','Nomor mesin tidak boleh sama!'),
    ]
    
    # ------------------------------ ARMADA ---------------------------------------------
    name             = fields.Char(string='Nama Armada', tracking=True)
    foto_mobil       = fields.Binary(string='Armada', tracking=True)
    merek_id         = fields.Many2one(comodel_name='cdn.merek', string='Merek Kendaraan', tracking=True)
    jumlah_kursi     = fields.Integer(string='Jumlah Kursi', default="2", tracking=True)
    jenis_armada     = fields.Selection(string='Jenis Armada', selection=[('bis', 'Bis Pariwisata'), ('travel', 'Travel'),('mobil', 'Mobil')], tracking=True)    
    tahun_pembuatan  = fields.Integer(string='Tahun Pembuatan', default=lambda self: date.today().year , tracking=True)
    no_plat          = fields.Char(string='Plat Nomor', tracking=True)
    no_mesin         = fields.Char(string='No Mesin', tracking=True)
    no_rangka        = fields.Char(string='No Rangka', tracking=True)
    jenis_kendaraan  = fields.Many2one(comodel_name='cdn.jenis.kendaraan', string='Jenis Kendaraan', domain="[('merek_id', '=', merek_id)]", tracking=True)

    # ------------------------------ KONDISI ARMADA ---------------------------------------------
    kondisi          = fields.Boolean(string='Kondisi Kendaraan', help="Jika aktif berarti armada dalam kondisi bagus", compute="_compute_kondisi", tracking=True)
    state            = fields.Selection(string='Status Armada', selection=[('tidak_siap','Tidak Siap'), ('dipakai', 'Sedang Dipakai'), ('siap', 'Siap Dipakai')])
    priority = fields.Selection([('0', 'Normal'),('1', 'Favorite'),], default='0', string="Favorite")

    # CREATED ALVITO
    # REVISI IAN
    # ------------------------------ HISTORY ARMADA ---------------------------------------------
    history_ids      = fields.One2many(comodel_name='cdn.history', inverse_name='armada_id', string='List Armada', tracking=True)
    tanggal_pakai    = fields.Date(string='Terakhir di pakai', compute = '_compute_tanggal_pakai', store = True)   
    km_akhir         = fields.Float(string='Kilometer Terakhir', compute = '_compute_kilometer_terakhir', store = True)   
    total_jarak      = fields.Integer(string='Total Jarak (km)', compute='_compute_total_jarak', store=True)

    # CREATED TRIADI
    # REVISI RIZKI
    # ------------------------------ SERVICE ARMADA ---------------------------------------------
    service_ids      = fields.One2many(comodel_name='cdn.service', inverse_name='armada_id', string='List Armada')
    hitung_service   = fields.Integer(string='Jumlah Service', compute="_compute_service_count", store=True)
    terakhir_service = fields.Date(string='Terakhir Service', compute='_compute_tanggal_service_terakhir', store=True)

    # CREATED ALVITO
    # REVISI RIZKI
    # ------------------------------ UJI KIR ARMADA ---------------------------------------------
    uji              = fields.Boolean(string='Uji', help="Jika aktif berarti armada dalam kondisi bagus", compute="_compute_uji" , tracking=True)  
    ujikir_ids       = fields.One2many(comodel_name='cdn.uji.kir', inverse_name='armada_id', string='List Uji Kir')
    berlaku_ujikir   = fields.Date(string='Berlaku Uji Kir', compute='_compute_tanggal_ujikir_terakhir', store=True)
    hitung_ujikir    = fields.Integer(string='Jumlah Service', compute="_compute_ujikir_count", store=True)

    @api.model
    def create(self, vals):
        # vals['kondisi']
        merek               = self.env['cdn.merek'].browse(vals.get('merek_id')).name
        jenis_kendaraan     = self.env['cdn.jenis.kendaraan'].browse(vals['jenis_kendaraan']).name
        vals['name']        = "[ %s ][ %s ] %s %s" % (vals['jenis_armada'], vals['no_plat'], merek, jenis_kendaraan)
        
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
    
    def write(self, vals):
        
        for record in self:
            merek_id = vals.get('merek_id', record.merek_id.id)
            jenis_kendaraan_id = vals.get('jenis_kendaraan', record.jenis_kendaraan.id)
            merek = self.env['cdn.merek'].browse(merek_id).name
            jenis_kendaraan = self.env['cdn.jenis.kendaraan'].browse(jenis_kendaraan_id).name
            vals['name'] = "[ %s ][ %s ] %s %s" % (record.jenis_armada, record.no_plat, merek, jenis_kendaraan)
        return super(CdnArmada, self).write(vals)

    @api.onchange('kondisi')
    def _onchange_kondisi(self): # fix bug rizki
        if  self.kondisi == True:
            self.state = 'siap'
        if  self.kondisi == False:
            self.state = 'tidak_siap'
        if self.kondisi not in (False, True): # jika kondisi tidak diisi
            self.state = 'tidak_siap'

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
                
    @api.depends('history_ids.km_akhir')
    def _compute_kilometer_terakhir(self):
        for rec in self:
            histori = self.env['cdn.history'].search([('armada_id', '=', rec.id)], order='id desc', limit=1)
            if histori:
                rec.km_akhir = histori.km_akhir
            else:
                rec.km_akhir = 0 # fix bug rizki
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
    

    def tombol_jenis(self):
        return {
            'name': _('Armada'),
            'res_model': 'cdn.armada',
            'view_mode': 'list,form,kanban',
            'context': {'default_jenis_armada':self.jenis_armada},
            'domain': [('jenis_armada','=',self.jenis_armada)],
            'type': 'ir.actions.act_window'
        }

    @api.depends('service_ids')
    def _compute_service_count(self):
        Jmlh = self.env['cdn.service']
        for rec in self:
            rec.hitung_service = Jmlh.sudo().search_count([('armada_id','=',rec.id)])
    
    @api.depends('ujikir_ids')
    def _compute_ujikir_count(self):
        Jmlh = self.env['cdn.uji.kir']
        for rec in self:
            rec.hitung_ujikir = Jmlh.sudo().search_count([('armada_id','=',rec.id)])

    @api.depends('history_ids.jarak')
    def _compute_total_jarak(self):
        for rec in self:
            total = sum(history.jarak for history in rec.history_ids)
            rec.total_jarak = total
            
    @api.depends('berlaku_ujikir')
    def _compute_uji(self):
        # state 
        for rec in self: 
            is_keadaan2 = None
            hari_ini2 = date.today()
            if rec.berlaku_ujikir : 
                if hari_ini2 <= rec.berlaku_ujikir:
                    is_keadaan2 = False
                else :
                    is_keadaan2 = True 
            rec.uji = is_keadaan2
    
    @api.depends('terakhir_service', 'state', 'service_ids')
    def _compute_kondisi(self):
        # state 
        for rec in self: 
            is_keadaan = None
            hari_ini = date.today()
            jangka_waktu = self.env['ir.config_parameter'].get_param('cdn_rental_armada.jangka_waktu')
            hari_batal_wajar = hari_ini - relativedelta.relativedelta(days=int(jangka_waktu))
            if rec.terakhir_service : 
                if rec.terakhir_service > hari_batal_wajar:
                    is_keadaan = False
                else :
                    is_keadaan = True
            rec.kondisi = is_keadaan

    # ------------------------------ ACTION ---------------------------------------------

    # CREATED RIZKI
    # ------------------------------ ACTION UJI KIR ---------------------------------------------
    def tombol_ujikir(self):
        action              = self.env["ir.actions.actions"]._for_xml_id("cdn_rental_armada.cdn_uji_kir_action")
        action['domain']    = [('armada_id', '=', self.id)]
        action['context']   = {'default_armada_id': self.id}
        return action
    
    # CREATED ALVITO
    # ------------------------------ ACTION HISTORY ---------------------------------------------
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

    # CREATED TRIADI
    # ------------------------------ ACTION SERVICE ---------------------------------------------
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
    def action_state_siap(self) :
        for rec in self : 
            rec.state = 'siap'

    def action_state_dipakai(self) :
        for rec in self : 
            rec.state = 'dipakai'

    def action_state_tidak_siap(self) :
        for rec in self : 
            rec.state = 'tidak_siap'

# CREATED BY TRIADI
# ------------------------------- JENIS ARMADA --------------------------------
class CdnjenisKendaraan(models.Model):
    _name        = 'cdn.jenis.kendaraan'
    _description = 'cdn jenis kendaraan'

    name         = fields.Char(string='Jenis Kendaraan', required=True)
    merek_id     = fields.Many2one(comodel_name='cdn.merek', string='Merek')


# CREATED BY TRIADI
# ------------------------------- MEREK --------------------------------
class CdnMerek(models.Model):
    _name        = 'cdn.merek'
    _description = 'Merek'
    
    name         = fields.Char(string='Nama', required=True)
    merek_logo   = fields.Image(string='Merek Logo')
    jenis_ids    = fields.One2many(comodel_name='cdn.jenis.kendaraan', inverse_name='merek_id', string='Jenis Kendaraan')