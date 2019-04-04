# -*- coding: utf-8 -*-
from odoo import models, fields, api

class NhaCungCap(models.Model):
    _name = 'nha.cungcap'
    _rec_name = 'name'

    name = fields.Char(string='Tên nhà cung cấp')
    add = fields.Char(string='Địa chỉ')
    sdt = fields.Char(string='Số điện thoại')
    website = fields.Char(string='Website')
    nguoi_dai_dien = fields.Char(string='Người đại diện')
    state = fields.Selection([('0','Bản thảo'),('1','Đã khóa')], default='0')

    @api.multi
    def action_nhacc_0_1(self):
        self.write({'state':'1'})

    @api.multi
    def action_nhacc_1_0(self):
        self.write({'state': '0'})
