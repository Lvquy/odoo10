# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import UserError


class ThietBi(models.Model):
    _name = 'thietbi'
    _rec_name = 'ma_thietbi'
    _inherit = 'mail.thread'


    cnect_linecheck = fields.Many2one('line.check')
    color = fields.Integer(default=0, store=True, compute='_color')
    ma_thietbi = fields.Char(string='Mã thiết bị', default='New', readonly=True)
    img = fields.Binary(string='Hình ảnh')
    type = fields.Selection([('pc','PC, Laptop'),
                             ('other','Khác'),
                             ('daughi','Đầu ghi hình')],
                            default='pc')
    nguoi_bao_quan = fields.Many2one('nguoi.baoquan',string='Người bảo quản', track_visibility='onchange')
    thoi_gian_mua = fields.Date(string='Thời gian mua')
    bao_hanh = fields.Char(string='Bảo hành(tháng)', track_visibility='onchange')
    bao_hanh_toi = fields.Date(string='Bảo hành tới', track_visibility='onchange')
    gia = fields.Integer(string='Giá trị', track_visibility='onchange', store=True)
    thuoc_tinh = fields.Many2many('thuoctinh',string='Thuộc tính')
    nha_cung_cap = fields.Many2one('nha.cungcap', string='Nhà cung cấp', track_visibility='onchange')
    vi_tri = fields.Char(string='Vị trí hiện tại', track_visibility='onchange')
    note =fields.Text(string='Ghi chú')
    nhat_ky_sua_chua = fields.One2many('line.nhatky','cnect_thiet_bi',string='Sửa chữa & thay thế')
    model_thiet_bi = fields.Char(string='Model')
    cpu = fields.Char('CPU', track_visibility='onchange')
    ram = fields.Char("RAM", track_visibility='onchange')
    hdd = fields.Char("HDD", track_visibility='onchange')
    ups = fields.Char("UPS", track_visibility='onchange')
    vga = fields.Char("VGA", track_visibility='onchange')
    keyb = fields.Char("Bàn phím", track_visibility='onchange')
    mouse = fields.Char("Chuột", track_visibility='onchange')
    monitor = fields.Char("Màn hình", track_visibility='onchange')
    mainb = fields.Char("MainB", track_visibility='onchange')
    power = fields.Char("Nguồn", track_visibility='onchange')
    syst = fields.Many2many('os',string="Hệ thống")
    ip_noibo = fields.Char(string='IP nội bộ')
    ip_ngoaibo = fields.Char(string='IP ngoại bộ')
    user_may = fields.Char(string='User máy')
    passw_may = fields.Char(string='Passw mở máy')
    status = fields.Selection([('1','Đang sử dụng'),
                               ('2', 'Trong kho'),
                               ('0', 'Phế')], default='2', track_visibility='onchange')
    ip = fields.Char(string='IP', track_visibility='onchange')
    domain_1 = fields.Char(string='Domain', track_visibility='onchange')
    port = fields.Char(string='Port', track_visibility='onchange')
    hdd_dau_ghi = fields.Char(string='HDD', track_visibility='onchange')
    ngo_vao = fields.Integer('Tổng ngõ vào')
    ngo_sd = fields.Integer('Số Ngõ sử dụng', track_visibility='onchange')
    tai_khoan = fields.Many2many('taikhoan',string='Tài khoản đăng nhập')
    adapter_mat = fields.Many2many('adapter.mat', string='Adapter & Mắt')
    total_daughi = fields.Integer('Tổng số đầu ghi')
    total_pc = fields.Integer('Tổng số máy tính')
    total_other = fields.Integer('Tổng các loại khác')
    total_adt = fields.Integer('Tổng adapter camera')
    total_mat = fields.Integer('Tổng mắt camera')

    @api.onchange('self')
    def _total_line(self):
        type_daughi = self.env['thietbi'].search([('type', '=', 'daughi')], limit=1)
        tong_daughi = 0
        for l in type_daughi:
            tong_daughi = sum(l)
        l.update({'total_daughi': tong_daughi})

    @api.depends('type')
    def _color(self):
        if self.type =='pc':
            self.color=5
        if self.type =='other':
            self.color =3
        if self.type =='daughi':
            self.color = 6


    # kho - sử dụng
    @api.multi
    def action_thietbi_2_1(self):
        if self.type =='pc':
            if self.nguoi_bao_quan:
                self.write({'status':'1'})
            else:
                raise UserError('Cần có người bảo quản')
        else:
            self.write({'status': '1'})
            for l in self.adapter_mat:
                l.status = '1'
            for k in self:
                for l in self.adapter_mat:
                    if l.status not in '0':
                        l.cho_daughi = k.id


    # sử dụng - phế
    @api.multi
    def action_thietbi_1_0(self):
        self.write({'status': '0'})
        for l in self.adapter_mat:
            l.status = '2'
            l.cho_daughi = [(6, 0, [])]
        self.nguoi_bao_quan = [(6, 0, [])]
        self.adapter_mat = [(6, 0, [])]

    # sử dụng - kho
    @api.multi
    def action_thietbi_1_2(self):
        self.write({'status': '2'})
        self.nguoi_bao_quan = [(6, 0, [])]
        for l in self.adapter_mat:
            l.cho_daughi = [(6,0,[])]
            if l.status not in '0':
                l.status = '2'
        self.adapter_mat = [(6, 0, [])]



    # tạo chỉ số chạy tự động
    @api.model
    def create(self, vals):
        # điều kiện, nếu get new = pc hoặc đâu ghi hoặc other và get type ='pc' thì return pc_code

        print vals.get('type','New')
        if ((vals.get('seq_pc_code', 'New') == 'New')
            or (vals.get('seq_daughi_code', 'New') == 'New')
            or (vals.get('seq_other_code', 'New') == 'New'))\
                and (vals.get('type', 'New') == 'pc'):

            vals['ma_thietbi'] = self.env['ir.sequence'].next_by_code('pc_code') or '/'
            return super(ThietBi, self).create(vals)
        if ((vals.get('seq_pc_code', 'New') == 'New')
            or (vals.get('seq_daughi_code', 'New') == 'New')
            or (vals.get('seq_other_code', 'New') == 'New'))\
                and (vals.get('type', 'New') == 'daughi'):
            vals['ma_thietbi'] = self.env['ir.sequence'].next_by_code('daughi_code') or '/'
            return super(ThietBi, self).create(vals)
        if ((vals.get('seq_pc_code', 'New') == 'New')
            or (vals.get('seq_daughi_code', 'New') == 'New')
            or (vals.get('seq_other_code', 'New') == 'New'))\
                and (vals.get('type', 'New') == 'other'):
            vals['ma_thietbi'] = self.env['ir.sequence'].next_by_code('other_code') or '/'
            return super(ThietBi, self).create(vals)