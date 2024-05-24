
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
    
    'depends': ['base', 'product', 'account', 'sale'],
    
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/armada.xml',
        'views/jenis_kendaraan.xml',
        'views/merek.xml',
        # 'views/kontak_inherit_view.xml',
        # 'views/karyawan.xml',
        'views/supir_view.xml',
        'views/tenaga_bantu.xml',
        'views/pengaturan.xml',
        # 'views/product_inherit.xml',
        'views/produk.xml',
        # 'views/penagihan_inherit.xml',
        'views/perawatan.xml',
        'reports/test_report.xml',
        'reports/travel_tersedia.xml',
        'reports/mobil_tersedia.xml',
        'reports/bus_tersedia.xml',
        'reports/semua_tersedia.xml',
        'views/pelanggan.xml',
        'views/transaksi.xml',
        # 'views/sale_order_line_inherit.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'aplication': True,
    

}