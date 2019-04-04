# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import datetime
from odoo.exceptions import UserError

class ThietBi(models.Model):
    _name = 'thiet.bi'
    _rec_name = 'name'
    _order = 'id desc'

    name = fields.Char(string='Tên thiết bị')
    ghi_chu = fields.Text(string='Ghi chú')
    gia_tri = fields.Integer(string='Giá trị')
    status = fields.Selection([('0','Bản thảo'),('1','Đã khóa')],string='Trạng thái', default='0')

    def lock_thietbi(self):
        self.status = '1'
    def unlock_thietbi(self):
        self.status = '0'

    @api.multi
    def unlink(self):
        for dem in self:
            if dem.status not in ('0'):
                raise UserError('Bạn không thể xóa thiết bị ở trạng thái đã khóa!')
        return super(ThietBi, self).unlink()

    class LineThietBi(models.Model):
        _name = 'line.thiet.bi'
        _rec_name = 'name'

        name = fields.Many2one('thiet.bi', string='Tên thiết bị')
        sl = fields.Integer(string='Số lượng')
        status = fields.Selection([('0','Mới'),('1','Cũ'),('2','Hỏng')],default='0', string='Tình trạng')
        ngay_kt = fields.Date(string='Ngày kiểm tra', default=datetime.today())
        note = fields.Text(string='Ghi chú')
        cnect_thietbi = fields.Many2one('phong.tro',string='kết nối')
