# -*- coding: utf-8 -*-
{
    'name': "Rental Armada",

    'summary': """
        Modul ini digunakan untuk mengelola data armada rental kendaraan 
        """,

    'description': """
        Aplikasi ini digunakan untuk mengelola data armada rental kendaraan dalam tugas cdn training
    """,

    'author': "CDN ARMADA TEAM",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'rental armada',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/armada.xml',
        'views/jenis_kendaraan.xml',
        'views/merek.xml',
        'views/kontak_inherit_view.xml',
        'views/karyawan.xml',
        'views/pengaturan.xml',
        'views/product_inherit.xml',
        'views/perawatan.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
