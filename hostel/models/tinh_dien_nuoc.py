# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.exceptions import UserError
from odoo import models,exceptions, fields, api,_
import json
import num2text


class TinhDienNuoc(models.Model):
    _name = 'dien.nuoc'
    _order = 'id desc'

    tien_thang = fields.Date(string='Tiền tháng', default = datetime.today())
    _sql_constraints = [
        ('tien_thang_uniq', 'unique (tien_thang)', "Tháng này đã tồn tại trong hệ thống !"),
    ]
    tong_thu_thang = fields.Integer(string='Tổng thu tháng này', readonly=True)
    doc_tien = fields.Char(string='Đọc tiền', store=True, compute="_doc_tien")
    status = fields.Selection([('0','Bản thảo'),('1','Đã xong')], default='0', string='Trạng thái')
    so_hoadon = fields.Char(string='Số hóa đơn', default='New', readonly=True)
    count_phong = fields.Integer(string='Số phòng thuê', store=True, compute='tinh_count')
    # khu_vuc = fields.Selection([('0','Tất cả'),('1','Khu 1'),('2','khu 2'),('3','Khu 3')],string='Khu vực', default='0')

    @api.depends('total_phong')
    def tinh_count(self):
        count = 0
        for i in self.total_phong:
            count += 1
        self.count_phong = count

    # tạo chỉ số chạy tự động
    @api.model
    def create(self, vals):
        vals['so_hoadon'] = self.env['ir.sequence'].next_by_code('invoice_code') or '/'
        return super(TinhDienNuoc, self).create(vals)

    @api.one
    @api.depends('tong_thu_thang')
    def _doc_tien(self):
        self.doc_tien = num2text.docso(self.tong_thu_thang) + u' đồng'

    @api.model
    def get_default_lines(self):
        list = []
        line_count = self.env['phong.tro'].search([('status', '=', 'khach')], order='id desc')
        for i in line_count:
            list.append([0, 0, {'phong': i.id,
                                'tien_phong': i.gia_phong,
                                'tien_khac': i.tien_khac,
                                'dien_old': i.cong_to_dien,
                                'nuoc_old': i.cong_to_nuoc
                                }])
        return list
    total_phong = fields.One2many('line.dien.nuoc','line_dn', string='Tất cả phòng', coppy=True, default=get_default_lines)
    def lock(self):
        a= True
        b=[]
        for i in self.total_phong:
            if i.status =='0':
                a = False
        if a is True:
            self.tong_thu_thang = 0
            for k in self.total_phong:
                self.tong_thu_thang += k.tong_tien
            self.status = '1'
        else:
            for j in self.total_phong:
                if j.status == '0':
                    b.append(j.phong.so_phong)
            b = json.dumps(b)
            raise exceptions.UserError(_('Chưa thu tiền xong các phòng %s') %b)
    def unlock(self):
        self.status = '0'
    @api.multi
    def unlink(self):
        for order in self:
            if order.status not in ('0'):
                raise UserError('Bạn không thể xóa!')
        self.total_phong.unlink()
        return super(TinhDienNuoc, self).unlink()

class LineDienNuoc(models.Model):
    _name = 'line.dien.nuoc'
    _rec_name = 'phong'

    line_dn = fields.Many2one('dien.nuoc',string='Kết nối')
    phong = fields.Many2one('phong.tro', string='Số phòng', readonly=True, required=True)
    dien_new = fields.Integer(string='Số điện mới')
    dien_old = fields.Integer(string='Số điện cũ')
    d_tieu_thu = fields.Integer(string='Số điện tiêu thụ', store=True, compute='tinh_dn')
    nuoc_new = fields.Integer(string='Số nước mới')
    nuoc_old = fields.Integer(string='Số nước cũ')
    n_tieu_thu = fields.Integer(string='Số nước tiêu thụ',store=True, compute='tinh_dn')
    tien_phong = fields.Integer(related='phong.gia_phong', string='Tiền phòng')
    tien_khac = fields.Integer(related='phong.tien_khac', string='Tiền khác')
    tong_tien = fields.Integer( string='Tổng tiền',store=True, compute='tinh_dn')
    status = fields.Selection([('0','Chưa xong'),('1','Đã thu')], default = '0', string='Trạng thái')
    # bank_acc_status = fields.Boolean(string='Khả dụng thanh toán bằng tài khoản',default=False, store=True, compute='_depends_bank')
    type_thu_tien = fields.Selection([('0','Tài khoản'),('1','Tiền mặt')], string='Kiểu thu tiền', readonly=True)
    note = fields.Text(string='Ghi chú')
    so_hoadon = fields.Char(string='Số hóa đơn', default='New', readonly=True)
    khu_vuc = fields.Selection(related="phong.khu_vuc", string="Khu vực", readonly=True)


    # tạo chỉ số chạy tự động
    @api.model
    def create(self, vals):
        vals['so_hoadon'] = self.env['ir.sequence'].next_by_code('line_invoice_code') or '/'
        return super(LineDienNuoc, self).create(vals)


    def get_def(self):
        self.chu_phong = self.phong.chu_phong
    chu_phong = fields.Many2one('khach.tro',string='Chủ phòng', readonly=True)
    so_du = fields.Integer(related='chu_phong.bank_acc', string='Số dư')

    @api.depends('dien_new','nuoc_new','dien_old','nuoc_old','tien_phong','tien_khac')
    @api.one
    def tinh_dn(self):
        if self.dien_new or self.nuoc_new:
            self.d_tieu_thu = self.dien_new - self.dien_old
            self.n_tieu_thu = self.nuoc_new - self.nuoc_old
            self.tong_tien = self.d_tieu_thu*self.phong.gia_dien + self.n_tieu_thu*self.phong.gia_nuoc + self.tien_khac + self.tien_phong

    @api.one
    def tru_tai_khoan(self):
        # print 'helo'
        if self.so_du >= self.tong_tien:
            self.chu_phong.bank_acc -= self.tong_tien
            self.status = '1'
            self.type_thu_tien = '0'
            self.phong.cong_to_dien = self.dien_new
            self.phong.cong_to_nuoc = self.nuoc_new

            vals = {
                'ma_khach': self.chu_phong.ma_khach,
                'so_tien': self.tong_tien,
                'name': self.chu_phong.name,
                'note': 'Trừ tiền phòng tháng %s' % datetime.today().month,
                'status': '1',
                'so_hoadon': self.so_hoadon

            }
            data = self.env['log.bank']
            data.create(vals)
        else:
            raise UserError('Số dư không đủ')

    def thu_tien_mat(self):
        self.status = '1'
        self.type_thu_tien = '1'
        self.phong.cong_to_dien = self.dien_new
        self.phong.cong_to_nuoc = self.nuoc_new

    @api.multi
    def unlock_status(self):
        self.env['dien.nuoc'].search([('total_phong.so_hoadon','=',self.so_hoadon)]).status = '0'
        self.status = '0'
        if self.type_thu_tien == '0':
            data = self.env['log.bank'].search([('so_hoadon', '=', self.so_hoadon), ('status', '=', '1')])
            if data:
                data.status = '2'
                self.chu_phong.bank_acc += self.tong_tien
    @api.multi
    def unlink(self):
        for order in self:
            if order.status not in ('0',):
                raise UserError('Bạn không thể xóa 1 Line khi ở trạng thái đã thu tiền!')
        return super(LineDienNuoc, self).unlink()