# -*- coding: utf-8 -*-
{
    "name": "Quản Lý Phòng Trọ",
    "author": "Lv Quý",
    "website": "tinyERP.net",
    "version":"1",
    "category":"Hostel",
    "license": "LGPL-3",
    "summary": "Phần mềm quản lý nhà trọ",
    "description": "Quản lý chuỗi nhà trọ thông minh bằng phần mềm",
    "depends": ['base','website','report','web_responsive'],
    "data": ['views/views.xml',
             'security/group.xml',
             'security/ir.model.access.csv',
             'views/view_phong.xml',
             'views/view_khach.xml',
             'views/view_thietbi.xml',
             'views/view_setting.xml',
             'views/view_dien_nuoc.xml',
             'data/demo_data.xml',
             'data/ir.seq_data.xml',
             'report/phieu_thu_k1.xml',
             'report/phieu_thu_k2.xml',
             'report/phieu_thu_k3.xml',
             'report/report_hoa_don_nap_tien.xml',
             'report/menu_report.xml'
             ]


}
