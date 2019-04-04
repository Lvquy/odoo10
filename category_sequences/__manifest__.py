# -*- coding: utf-8 -*-
{
    'name': "Category Sequences",

    'summary': """ Category Sequences For TinyERP.net """,

    'description': """
        Category Sequences For TinyERP.net 
        1.在类别中新增类别编码字段，并且建立类别相对应序列。
        2.新建产品会自动按类别编码，建立物料编码，并且加入序列，且不重复。
        3.新增产品状态。草稿、锁定、取消。
           草稿：产品Active 为False，可以修改，系统未能使用它。
           锁定：产品Active 为Ture，不可修改类别和物料编码。系统可使用它。
           取消：产品Active 为False，此产品取消，系统不可使用它。
    """,

    'author': "WANG ZHAO HUA",
    'website': "http://www.tinyerp.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tiny ERP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'data/cate_seq_data.xml',
        'data/product_cate_seq_data.xml',
        'data/partner_seq_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
}
