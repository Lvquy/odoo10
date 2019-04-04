# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError
import num2text


class KhachTro(models.Model):
    _name = 'khach.tro'
    _rec_name = 'name'
    _order = 'id desc'

    img = fields.Binary(string='Hình ảnh')
    name = fields.Char(string='Tên khách', required=True)
    ma_khach = fields.Char(string='Mã khách', required=True, default='New', readonly=True)
    mobile = fields.Char(string='Số điện thoại')
    add = fields.Text(string='Địa chỉ')
    gioi_tinh = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ'), ('khac', 'Khác')], string='Giới tính')
    ngay_toi = fields.Date(string='Ngày tới thuê', default=datetime.today())
    ngay_tra = fields.Date(string='Ngày trả phòng')
    bank_acc = fields.Integer(string='Tài khoản(VNĐ)', default=0, readonly=True)
    status = fields.Selection([('0', 'Nháp'), ('1', 'Đã khóa'), ('2', 'Đang thuê'), ('3', 'Đã trả phòng')], default='0')
    mobile_ngthan = fields.Char(string='Số điện thoại người thân')
    add_new = fields.Integer(string='Số tiền nạp')
    doc_tien = fields.Char(string='Đọc tiền', store=True, compute="_doc_tien")
    dang_o = fields.Char(string='Đang thuê phòng', readonly=True)
    cmnd = fields.Char(string='Số CMND', required=True)
    _sql_constraints = [
        ('cmnd_uniq', 'unique (cmnd)', "Số CMND này đã tồn tại trong hệ thống !"),
    ]

    @api.one
    @api.depends('bank_acc')
    def _doc_tien(self):
        if self.bank_acc < 0:
            self.bank_acc =0
        self.doc_tien = num2text.docso(self.bank_acc) + u' đồng'


    def xacnhan0_1(self):
        self.status = '1'

        # def xacnhan1_2(self):
        #     self.status = '2'
        #
        # def xacnhan2_3(self):
        #     self.status = '3'

    # tạo chỉ số chạy tự động
    def set_0(self):
        self.bank_acc = 0
    @api.model
    def create(self, vals):
        vals['ma_khach'] = self.env['ir.sequence'].next_by_code('khach_code') or '/'
        return super(KhachTro, self).create(vals)

    @api.multi
    def unlink(self):
        for i in self:
            if i.status == '2':
                raise UserError('Khách này đang ở trọ, bạn không thể xóa!')
        return super(KhachTro, self).unlink()

    # def _check_qty(self):
    #     min = 0
    #     max = 100000000
    #     # if min > self.bank_acc > max:
    #     #     raise UserError('Chấp nhận trong khoảng 0-100 triệu')
    #     if min <= self.bank_acc < max: return False
    #     return True
    # _constraints = [(_check_qty, 'Số tiền cho phép trong khoảng 0-100 triệu !', ['bank_acc'])]


class Naptien(models.Model):
    _name = 'nap.tien'
    _order = 'id desc'
    _rec_name = 'ma_khach'

    so_tien = fields.Integer(string='Số tiền nạp', size='2')
    ngay_nap = fields.Date(string='Ngày nạp', default=datetime.today())
    ngay_tao_hoa_don = fields.Datetime(string='Ngày tạo hóa đơn', readonly=True, default=datetime.today())
    ten_khach = fields.Many2one('khach.tro', string='Tên người thụ hưởng', required=True)
    note = fields.Text(string='Ghi chú cho hóa đơn')
    doc_tien = fields.Char(string='Đọc tiền', store=True, compute="_doc_tien")
    nhan_vien = fields.Many2one('res.users', string='Người phụ trách', readonly=True,
                                default=lambda self: self.env.user)
    cmnd = fields.Char(related='ten_khach.cmnd',string='Số CMND', readonly=True)
    ma_giaodich = fields.Char(string='Mã giao dịch',readonly=True,default='New')

    # tạo chỉ số chạy tự động
    @api.model
    def create(self, vals):
        vals['ma_giaodich'] = self.env['ir.sequence'].next_by_code('naptien_code') or '/'
        return super(Naptien, self).create(vals)

    @api.one
    @api.depends('so_tien')
    def _doc_tien(self):
        if self.so_tien<0:
            self.so_tien = 0
        self.doc_tien = num2text.docso(self.so_tien) + u' đồng'

    def add_5(self):
        self.so_tien += 5000

    def add_10(self):
        self.so_tien += 10000

    def add_50(self):
        self.so_tien += 50000

    def add_100(self):
        self.so_tien += 100000

    def add_200(self):
        self.so_tien += 200000

    def add_500(self):
        self.so_tien += 500000

    def reset(self):
        self.so_tien = 0

    ma_khach = fields.Char(related='ten_khach.ma_khach', string='Mã khách')
    note = fields.Text(string='Ghi chú')
    status = fields.Selection([('0', 'Bản thảo'), ('1', 'Đã xác nhận')], string='Trạng thái', default='0')

    def lock(self):
        self.ten_khach.bank_acc += self.so_tien
        self.status = '1'

    def unlock(self):
        self.ten_khach.bank_acc -= self.so_tien
        self.status = '0'
    # @api.multi
    # def unlink(self):
    #     for i in self:
    #         if i.status not in '0':
    #             raise UserError('Bạn không thể xóa chứng từ ở trạng thái đã xác nhận')
    #     return super(Naptien, self).unlink()
    # def _check_qty(self):
    #     min = 0
    #     max = 100000000
    #     # if  min > self.so_tien > max:
    #     #     raise UserError('Chấp nhận trong khoảng 0-100 triệu')
    #     if min <= self.so_tien < max: return False
    #     return True
    # _constraints = [(_check_qty, 'Số tiền cho phép trong khoảng 0-100 triệu !', ['so_tien'])]


class Log_bank(models.Model):
    _name = 'log.bank'
    _rec_name = 'ma_khach'
    _order = 'id desc'

    ma_khach = fields.Char(string='Mã khách')
    name = fields.Char(string='Khách trọ')
    so_tien = fields.Integer(string='Số tiền trừ')
    note = fields.Text(string='Ghi chú cho hóa đơn')
    ngay = fields.Datetime(string='Ngày tạo hóa đơn', default=datetime.today())
    status = fields.Selection([('0', 'Nháp'), ('1', 'Đã khóa'), ('2', 'Đã hoàn trả')], default='0', string='Trạng thái')
    so_hoadon = fields.Char(string='Chứng từ', readonly=True)

    @api.multi
    def un_bank(self):
        khach = self.env['khach.tro'].search([('ma_khach', '=', self.ma_khach)])
        khach.bank_acc += self.so_tien
        self.status = '2'
        data = self.env['line.dien.nuoc'].search([('so_hoadon','=',self.so_hoadon)])
        if data:
            data.status = '0'
            data.type_thu_tien = False

    # @api.multi
    # def unlink(self):
    #     for i in self:
    #         if i.status not in '0':
    #             raise UserError('Bạn không thể xóa chứng từ ở trạng thái đã xác nhận')
    #     return super(Log_bank, self).unlink()