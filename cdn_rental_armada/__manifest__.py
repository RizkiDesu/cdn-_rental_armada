
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
    
    'depends': ['base', 'mail','product', 'account', 'sale', 'stock','website' ],
    
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',

        'data/sequence_data.xml',
        'data/ir_config_parameter.xml',


        
        'data/navbar_site.xml',
        'views/home_page_site.xml',
        # 'data/test_ambil.xml',
        'views/armada_site.xml',
        'views/produk_site.xml',
        'views/form_pendaftaran_site.xml',
        'views/form_booking_site.xml',

        
        'reports/report_booking.xml',
        'reports/test_report.xml',
        'reports/travel_tersedia.xml',
        'reports/mobil_tersedia.xml',
        'reports/bus_tersedia.xml',
        'reports/semua_tersedia.xml',

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
        'views/pelanggan.xml',

        'views/produk.xml',
        'views/account_move.xml',
        'views/pemesanan.xml',
        'views/penagihan_line.xml',
        'reports/inherit_report.xml',

        # 'views/varian.xml',
        'views/account_move.xml',
        'views/pemesanan.xml',
        'views/denda.xml',
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
    'assets': {
        'web.assets_frontend': [
            '/cdn_rental_armada/static/src/css/bootstrap.min.css',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css',
            '/cdn_rental_armada/static/src/liba/owlcarousel/assets/owl.carousel.min.css',
            '/cdn_rental_armada/static/src/liba/tempusdominus/css/tempusdominus-bootstrap-4.min.css',
            '/cdn_rental_armada/static/src/css/style.css',
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js',
            '/cdn_rental_armada/static/src/liba/easing/easing.min.js',
            '/cdn_rental_armada/static/src/liba/waypoints/waypoints.min.js',
            '/cdn_rental_armada/static/src/liba/owlcarousel/owl.carousel.min.js',
            '/cdn_rental_armada/static/src/liba/tempusdominus/js/moment.min.js',
            '/cdn_rental_armada/static/src/liba/tempusdominus/js/moment-timezone.min.js',
            '/cdn_rental_armada/static/src/liba/tempusdominus/js/tempusdominus-bootstrap-4.min.js',
            '/cdn_rental_armada/static/src/jees/main.js',
            '/cdn_rental_armada/static/src/jees/selectt.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
            
        ],
    },
    'aplication': True,
    

}