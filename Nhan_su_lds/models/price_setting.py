# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class Setting(models.Model):
    _name = 'setting'
    _rec_name = 'name'

    name=fields.Char(string='Name',default='Cài đặt giá mặc định cho hệ thống', readonly=True)

    man_4 = fields.Integer(string='Giá suất mặn 4 tiếng')
    chay_4 = fields.Integer(string='Giá suất chay 4 tiếng')
    chao_4 = fields.Integer(string='Giá suất cháo 4 tiếng')

    chao_3 = fields.Integer(string='Giá suất cháo 3 tiếng')
    chay_3 = fields.Integer(string='Giá suất chay 3 tiếng')
    man_3 = fields.Integer(string='Giá suất mặn 3 tiếng')
    dac_biet = fields.Integer(string='Giá suất đặc biệt')

    bun = fields.Integer(string='Giá suất bún')

    sang1_h = fields.Integer(help="Giờ cho phép bắt đầu báo cơm trong ngày")
    sang1_m = fields.Integer(help="Phút")

    sang2_h = fields.Integer(string="Sáng 2 giờ", help="Giờ giói hạn cho phép báo cơm buổi sáng, nếu qua giờ này sẽ không cho phép báo cơm")
    sang2_m = fields.Integer(string="Sáng 2 phút", help="phút")

    chieu2_h = fields.Integer(string="Chiều 2 giờ", help="Giờ giới hạn cho phép báo cơm chiều, nếu quá thời gian này sẽ không cho phép báo cơm chiều")
    chieu2_m = fields.Integer(string="Chiều 2 phút", help="phút")
    status = fields.Selection([('0','Bản thảo'),('1','Đã khóa')],string="Trạng thái",default='0')

    # def _check_name(self):
    #     for val in self.read(['name']):
    #         if val['name']:
    #             if len(val['name']) < 6:
    #                 return False
    #
    #         return True
    #
    # _constraints = [(_check_name, 'Name must have at least 6 characters.',['name'])]

    @api.model
    def create(self, vals):
        count = self.env['setting'].search_count([])
        # print count,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        if count >=1:
            # print 'da ton tai cau hinh roi'
            raise UserError('Lỗi! Không được phép tạo nhiều hơn 1 cấu hình.')
        # print '*****************'
        return super(Setting, self).create(vals)

    @api.multi
    def unlink(self):
        if self.env['setting'].search_count([])<=1:
            raise UserError('Nếu xóa cấu hình, hệ thống sẽ bị lỗi')
        return super(Setting, self).unlink()
    @api.multi
    def lock_stt(self):
        if self.status =='1':
            self.status = '0'
        else:
            self.status = '1'








