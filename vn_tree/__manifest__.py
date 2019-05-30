# -*- coding: utf-8 -*-

{
    "name": "Cây địa chỉ tỉnh Việt Nam",
    "summary": "Hiển thị phân cấp địa chỉ các tỉnh Việt Nam",
    "version": "",
    "category": "custom",
    "website": "https://tinyerp.net/",
    "author": "Lv Quy",
    "license": "LGPL-3",
    "depends": ['base','hr'
                ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/tinh.xml',
        'data/huyen.xml',
        'data/xa1.xml',
        'data/xa2.xml',
        'data/xa3.xml',
        'views/view_add.xml',
        'views/view_employee.xml',
    ],
    'qweb': [],
    'application'   : True,
    'auto_install'  : False,
}
