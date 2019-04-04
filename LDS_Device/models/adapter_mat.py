# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, date

class AdapterMat(models.Model):
    _name = 'adapter.mat'
    _rec_name = 'ma_so'
    _inherit = 'mail.thread'

    ma_so = fields.Char(string='Mã số', default='New',readonly=True)
    type = fields.Selection([('ad','Adapter'),('mat','Mắt')])
    model = fields.Char(string='Model')
    status = fields.Selection([('1', 'Đang sử dụng'),
                               ('2', 'Trong kho'),
                               ('0', 'Phế')], default='2', track_visibility='onchange')
    cho_daughi = fields.Many2one('thietbi',string='Cho đầu ghi', track_visibility='onchange')
    state = fields.Selection([('0','Bản thảo'),('1','Đã khóa')], default='0', track_visibility='onchange')
    ngay_bao_phe = fields.Date(string='Ngày báo phế')
    ngay_mua = fields.Date(string='Ngày mua', default = lambda s: date.today())
    bao_hanh = fields.Integer(string='Bảo hành(Tháng)')
    bao_hanh_toi = fields.Date(string='Bảo hành tới')
    gia_tri = fields.Integer(string='Giá trị', default=0)
    nha_cc = fields.Many2one('nha.cungcap', string='Nhà cung cấp')
    note = fields.Text(string='Ghi chú')
    @api.multi
    def action_state_0_1(self):
        self.write({'state':'1'})

    # kho - sử dụng
    @api.multi
    def action_adt_2_1(self):
        if self.cho_daughi:
            self.write({'status': '1'})
        else:
            raise UserError('Thiếu trường "Cho đầu ghi"!')

    # sử dụng - phế
    @api.multi
    def action_adt_1_0(self):
        self.write({'status': '0'})
        self.cho_daughi = [(6, 0, [])]
        self.ngay_bao_phe = datetime.now()

    # sử dụng - kho
    @api.multi
    def action_adt_1_2(self):
        self.write({'status': '2'})
        self.cho_daughi = [(6, 0, [])]

    # tạo chỉ số chạy tự động
    @api.model
    def create(self, vals):
        if ((vals.get('seq_mat_code', 'New') == 'New') or (vals.get('seq_adapter_code', 'New') == 'New'))\
                and (vals.get('type', 'New') == 'ad'):
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('adapter_code') or '/'
            return super(AdapterMat, self).create(vals)

        if ((vals.get('seq_mat_code', 'New') == 'New') or (vals.get('seq_adapter_code', 'New') == 'New'))\
                and (vals.get('type', 'New') == 'mat'):
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('mat_code') or '/'
            return super(AdapterMat, self).create(vals)