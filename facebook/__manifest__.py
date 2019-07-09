# -*- coding: utf-8 -*-

{
    "name": "FACEBOOK",
    "summary": "API FB",
    "version": "",
    "category": "API FB",
    "website": "https://tinyerp.net",
    "author": "Lv Quy",
    "license": "LGPL-3",
    "depends": ['sale'
                ],
    "data": [
        'views/view.xml',
        'views/linefb.xml',
        'views/setting.xml',
        'views/get_id.xml',
        'views/new_user.xml',
    ],
    'qweb': [],
    'application'   : True,
    'auto_install'  : False,
}