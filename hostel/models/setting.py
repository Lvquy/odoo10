# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import datetime
from odoo.exceptions import UserError

class Setting(models.Model):
    _name = 'setting.hostel'
    _order = 'id desc'

    name = fields.Char(string='Tên cấu hình')
    status = fields.Selection([('0','Bản thảo'),('1','Đã kích hoạt')],string='Trạng thái', default='0')

    gia_dien_k1 = fields.Integer(string='Giá điện khu 1')
    gia_dien_k2 = fields.Integer(string='Giá điện khu 2')
    gia_dien_k3 = fields.Integer(string='Giá điện khu 3')

    gia_nuoc_k1 = fields.Integer(string='Giá nước khu 1')
    gia_nuoc_k2 = fields.Integer(string='Giá nước khu 2')
    gia_nuoc_k3 = fields.Integer(string='Giá nước khu 3')

    gia_phong_k1 = fields.Integer(string='Giá phòng khu 1')
    gia_phong_k2 = fields.Integer(string='Giá phòng khu 2')
    gia_phong_k3 = fields.Integer(string='Giá phòng khu 3')

    tien_khac_k1 = fields.Integer(string='Tiền khác khu 1')
    tien_khac_k2 = fields.Integer(string='Tiền khác khu 2')
    tien_khac_k3 = fields.Integer(string='Tiền khác khu 3')

    def lock(self):
        data = self.search([('status', '=', '1')], order='id desc')
        for i in data:
            i.status = '0'
        self.status = '1'

        count = self.search_count([])
        # print count
        if count > 2:
            data1= self.search([('status','!=','1')],order='id asc')
            print 'sau khi go',data1
            for j in data1:
                super(Setting, j).unlink()
    def unlock(self):
        self.status='0'

    @api.multi
    def unlink(self):
        for i in self:
            if i.status not in '0':
                raise UserError('Không thể xóa một cấu hình đang kích hoạt!')
        return super(Setting, self).unlink()



