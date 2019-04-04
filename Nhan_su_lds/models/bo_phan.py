# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class BoPhanUser(models.Model):
    _inherit = 'res.users'
    # bo_phan = fields.Char(string='Bộ phận', store=True)
    bo_phan = fields.Selection([
        ('VPHONG','Văn phòng'),
        ('TMAY', 'Tổ máy'),
        ('CNC', 'CNC'),
        ('CN1', 'Chà nhám 1'),
        ('CN2', 'Chà nhám 2'),
        ('MAU', 'Tổ mẫu'),
        ('VECNI', 'Vecni'),
        ('LRAP', 'Lắp ráp'),
        ('CTRINH', 'Công trình'),
        ('TDO', 'Tiến độ'),
        ('KHO', 'Kho'),
        ('QC','QC'),
        ('BTRI', 'Bảo trì'),
        ('IT', 'IT')
                                ],string='Bộ phận',store=True)