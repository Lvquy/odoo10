# -*- coding: utf-8 -*-
{
    'name': "LDS Report",

    'summary': """ LDS Report For CTY """,

    'description': """
        LDS Report For CTY CP LAM DAT HUNG
    """,

    'author': "BP IT, QUY",
    'website': "http://www.ldsvn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    # update 15-03-2018
    'category': 'LDS Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'purchase','report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'purchase_report/lds_purchase_order.xml',
        'purchase_report/lds_purchase_order_en.xml',
        'stock_report/lds_report_deliveryslip.xml',
        'stock_report/lds_report_stockpicking.xml',
        'sale_report/lds_sale_report.xml',
        'sale_report/lds_sale_pac_report.xml',
        'account_invoice/lds_report_intrastat_invoice.xml',
		'account_invoice/lds_report_intrastat_invoice_1.xml',
        # 'data/wr_sequence_data.xml',
    ],
    'qweb': [
        'purchase_report/lds_purchase_order.xml',
        'purchase_report/lds_purchase_order_en.xml',
        'stock_report/lds_report_deliveryslip.xml',
        'stock_report/lds_report_stockpicking.xml',
        'sale_report/lds_sale_report.xml',
        'sale_report/lds_sale_pac_report.xml',
        'account_invoice/lds_report_intrastat_invoice.xml',
		'account_invoice/lds_report_intrastat_invoice_1.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
