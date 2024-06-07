
{
    'name': 'Rental Armada',
    'version': '1.0.0',
    'summary': """
        Rental Armada Untuk Perusahaan Travel""",
    'description': """
        Membuat module odoo16 Rental Armada
    """,
    'category': 'Uncategorized',
    'author': 'Armada Team',
    'maintainer': 'armada_team',
    'website': 'https://www.website.com',
    'license': 'AGPL-3',
    
    'depends': ['base', 'mail','product', 'account', 'sale', 'stock' ],
    
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'views/menu_view.xml',
        'views/armada.xml',
        'views/jenis_kendaraan.xml',
        'views/merek.xml',
        'views/supir_view.xml',
        'views/tenaga_bantu.xml',
        'views/pengaturan.xml',
        'views/uji_kir_view.xml',
        'views/perawatan.xml',
        'views/history.xml',
        'reports/report_booking.xml',
        'reports/test_report.xml',
        'reports/travel_tersedia.xml',
        'reports/mobil_tersedia.xml',
        'reports/bus_tersedia.xml',
        'reports/semua_tersedia.xml',
        'views/pelanggan.xml',
        'data/sequence_data.xml',
        'views/varian.xml',
        'views/account_move.xml',
        'views/pemesanan.xml',
        'views/penagihan_line.xml',
        'reports/inherit_report.xml',
        'views/varian.xml',
        'views/account_move.xml',
        'views/pemesanan.xml',
        'wizards/pengembalian_armada.xml',

        
        'views/wilayah/kecamatan.xml',
        'views/wilayah/desa.xml',
        'views/wilayah/kota.xml',
        'views/wilayah/propinsi.xml',
        'views/wilayah/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'aplication': True,
    

}