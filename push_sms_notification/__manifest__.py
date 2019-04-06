# -*- coding: utf-8 -*-
{
    "name": "Push SMS Notification",
    "summary":"",
    "author":"Lv Quy",
    "license":'LGPL-3',
    "description":'''Push sms, to customer, vendor''',
    "depends":['purchase'],
    "data":[
        'views/view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application'   : True,
    'auto_install'  : False,
}