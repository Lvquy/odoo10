# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import datetime
from odoo.exceptions import UserError

class PhongTro(models.Model):
    _name = 'phong.tro'
    _rec_name = 'so_phong'
    _order = 'id desc'

    so_phong = fields.Char(string='Số phòng', required=True)
    khu_vuc = fields.Selection([('k1','Khu 1'),('k2','Khu 2'),('k3','Khu 3')],string='Khu vực', required=True)
    status = fields.Selection([('trong','Trống'),('khach','Có khách')],string='Trạng thái phòng', default='trong')
    khach_tro = fields.One2many('line.khach','cnect_phong_khach',string='Khách trọ')
    hop_dong = fields.Html(string='Hợp đồng & điều khoản')
    color = fields.Integer(string='Màu',default=1, compute='_get_color')
    img = fields.Binary(string='Ảnh chủ phòng', store=True, compute='get_img')

    @api.depends('chu_phong')
    def get_img(self):
        if self.chu_phong:
            self.img = self.chu_phong.img

    @api.one
    @api.depends('state')
    def _get_color(self):
        if self.state == '0':
            self.color = 1
        if self.state == '1':
            self.color = 5

    def get_default_price(self):
        data = self.env['setting.hostel'].search([('status','=','1')], limit=1, order='id desc')
        if self.khu_vuc == 'k1':
            self.gia_phong = data.gia_phong_k1
            self.gia_dien = data.gia_dien_k1
            self.gia_nuoc = data.gia_nuoc_k1
            self.tien_khac = data.tien_khac_k1
        if self.khu_vuc == 'k2':
            self.gia_phong = data.gia_phong_k2
            self.gia_dien = data.gia_dien_k2
            self.gia_nuoc = data.gia_nuoc_k2
            self.tien_khac = data.tien_khac_k2
        if self.khu_vuc == 'k3':
            self.gia_phong = data.gia_phong_k3
            self.gia_dien = data.gia_dien_k3
            self.gia_nuoc = data.gia_nuoc_k3
            self.tien_khac = data.tien_khac_k3

    gia_phong = fields.Integer(string='Giá phòng')
    gia_dien = fields.Integer(string='Giá điện')
    gia_nuoc = fields.Integer(string='Giá nước')
    tien_khac = fields.Integer(string='Tiền khác', help="Có thể là tiền vệ sinh hoặc tiền cộng thêm hay trừ đi")

    cong_to_dien = fields.Integer(string='Số công tơ điện')
    cong_to_nuoc = fields.Integer(string='Số công tơ nước')
    ngay_khach_vao = fields.Date(string='Ngày khách vào')
    ngay_khach_tra = fields.Date(string='Ngày khách trả')
    state = fields.Selection([('0','Nháp'),('1','Đã khóa')], default='0', string='Trạng thái')
    thiet_bi = fields.One2many('line.thiet.bi','cnect_thietbi',string='Thiết bị')
    chu_phong = fields.Many2one('khach.tro', string='Chủ phòng')
    ma_chu_phong = fields.Char(related='chu_phong.ma_khach',string='Mã khách')
    def lock_state(self):
        self.state = '1'
    def unlock_state(self):
        self.state= '0'

    def lock_phong(self):
        if self.khach_tro:
            for i in self.khach_tro:
                print i.line_khach.name
                i.line_khach.status = '2'
                i.line_khach.dang_o = self.so_phong
            self.ngay_khach_vao = datetime.today()
            self.status = 'khach'
            self.ngay_khach_tra = False

        else:
            raise UserError('Chưa thêm khách vào phòng!')
    @api.one
    def unlock_phong(self):
        for i in self.khach_tro:
            print i.line_khach.name
            i.line_khach.status = '3'
            i.line_khach.dang_o = ''
            i.line_khach.ngay_tra = datetime.today()
        self.chu_phong = False
        self.khach_tro = False
        self.status = 'trong'
        self.ngay_khach_tra = datetime.today()
        self.ngay_khach_vao = False

    @api.multi
    def unlink(self):
        for i in self:
            if i.status not in 'trong':
                raise UserError('Đang có khách trong phòng, không thể xóa!')

        data = self.env['line.dien.nuoc'].search([('status','=','1')])
        for i in data:
            print i.phong.so_phong, self.so_phong
            if i.phong.so_phong == self.so_phong:
                raise UserError('Bạn không thể xóa!, phòng này đang được tham chiếu')
        return super(PhongTro, self).unlink()


class LineKhach(models.Model):
    _name = 'line.khach'
    _rec_name = 'line_khach'

    ma_khach = fields.Char(related='line_khach.ma_khach', string='Mã khách')
    line_khach = fields.Many2one('khach.tro',string='Tên khách')
    dien_thoai = fields.Char(related='line_khach.mobile',string='Số điện thoại')
    bank_acc = fields.Integer(related='line_khach.bank_acc',string='Số dư', readonly=True)
    cnect_phong_khach = fields.Many2one('phong.tro', string='Liên kết tới phòng trọ')

    @api.multi
    def unlink(self):
        if self.line_khach.status == '2':
            raise UserError('khach dang thue')