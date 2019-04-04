# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import datetime, date

class LogCheck(models.Model):
    _name = 'log.check'
    _rec_name = 'ngay'
    _order = 'id desc'

    ngay = fields.Datetime(string='Ngày kiểm tra', default = lambda s: datetime.now())

    @api.model
    def get_default_lines(self):
        list = []
        line_count = self.env['thietbi'].search([('type','=','daughi'),('status','=','1')])# đếm số đầu ghi hiện có
        for i in line_count:
            list.append([0, 0, {'line_check':i.id,
                                'check':False,
                                'vi_tri':i.vi_tri
                                }])
        return list

    device = fields.One2many('line.check', 'cnect_logcheck', string='Thiết bị', coppy=True, default = get_default_lines)
    count_error = fields.Integer('Số đầu ghi bị lỗi', store=True, compute='tinh_error')

    @api.depends('device')
    def tinh_error(self):
        cout = 0
        for i in self.device:
            if i.check == True:
                cout +=1
                self.write({'i.line_check.color': 1})
        self.count_error = cout
