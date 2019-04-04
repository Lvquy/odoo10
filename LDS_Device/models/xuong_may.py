# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import UserError


class XuongMay(models.Model):
    _name = 'xuong.may'
    _rec_name = 'ma_so'
    _inherit = 'mail.thread'


    ma_so = fields.Char(string='Mã số', default='New', readonly=True)
    name = fields.Char(string='Tên máy',track_visibility='onchange', required=True)
    cty = fields.Selection([('lds','Lâm Đạt Hưng'),('nt','Nhật Tâm')], string='Công ty', default='lds')
    bo_phan = fields.Selection([('cnc','CNC'),
                                ('tm','Tổ máy'),
                                ('cn1','C.Nhám 1'),
                                ('cn2', 'C.Nhám 2'),
                                ('m', 'Tổ mẫu'),
                                ('s', 'Tổ Sơn'),
                                ('x2', 'Xưởng 2'),
                                ],string='Bộ phận',track_visibility='onchange', required=True)
    gia_tri = fields.Integer(string='Giá trị máy',track_visibility='onchange')
    ngay_sd = fields.Date(string='Ngày sử dụng',track_visibility='onchange')
    ngay_phe = fields.Date(string='Ngày báo phế',track_visibility='onchange')
    nguoi_bao_quan = fields.Many2one('nguoi.baoquan', string='Người bảo quản',track_visibility='onchange')
    ghi_chu = fields.Text(string='Ghi chú')
    img = fields.Binary(string='Hình ảnh')
    sua_chua = fields.One2many('line.nhatky','cnect_xuongmay', string='Sửa chữa & thay thế')
    status = fields.Selection([('0','Bản thảo'),('1','Đã khóa')], string='Trạng thái', default='0')
    trang_thai = fields.Selection([('1','Đang sử dụng'),('2','Trong kho'),('0','Phế')],string='Trạng thái', default='2')
    color = fields.Integer(string='Màu sắc', default=0,store=True, compute='_setcolor')
    # ngay_baotri = fields.Date(string='Ngày bảo trì')
    # chu_ky = fields.Integer(string='Chu kỳ (Tháng)', default=1)
    # da_baotri = fields.Boolean(string='Cần bảo trì', default=False)

    @api.depends('cty')
    def _setcolor(self):
        if self.cty =='lds':
            self.color = 5
        if self.cty =='nt':
            self.color = 7


    @api.multi
    def lock(self):
        self.write({'status':'1'})

    # tạo chỉ số chạy tự động
    @api.model
    def create(self, vals):
        if vals.get('bo_phan','New') =='cnc':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('xuong_cnc_code') or '/'
            return super(XuongMay, self).create(vals)
        if vals.get('bo_phan', 'New') == 'tm':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('xuong_tm_code') or '/'
            return super(XuongMay, self).create(vals)
        if vals.get('bo_phan', 'New') == 'cn1':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('xuong_cn1_code') or '/'
            return super(XuongMay, self).create(vals)
        if vals.get('bo_phan', 'New') == 'cn2':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('xuong_cn2_code') or '/'
            return super(XuongMay, self).create(vals)
        if vals.get('bo_phan', 'New') == 'm':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('xuong_m_code') or '/'
            return super(XuongMay, self).create(vals)
        if vals.get('bo_phan', 'New') == 's':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('xuong_s_code') or '/'
            return super(XuongMay, self).create(vals)
        if vals.get('bo_phan', 'New') == 'x2':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('xuong_x2_code') or '/'
            return super(XuongMay, self).create(vals)

    @api.multi
    def action_2_1(self):
        self.write({'trang_thai':'1'})

    @api.multi
    def action_1_2(self):
        self.write({'trang_thai': '2'})

    @api.multi
    def action_1_0(self):
        self.write({'trang_thai': '0'})
        self.ngay_phe = date.today()
