# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date

class LineNhatKy(models.Model):
    _name = 'line.nhatky'
    _rec_name = 'so_nhat_ki'
    _inherit = 'mail.thread'

    cnect_thiet_bi = fields.Many2one('thietbi')
    cnect_xuongmay = fields.Many2one('xuong.may')
    so_nhat_ki = fields.Char(string='Số nhật ký', default='New', readonly=True)

    status = fields.Selection([('0','Đang sửa'),('1','Đã xong')],default='0', track_visibility='onchange')
    thoi_gian_sua = fields.Date(string='Thời gian bắt đầu sửa', track_visibility='onchange')
    thoi_gian_hoan_thanh = fields.Date(string='Thời gian hoàn thành', track_visibility='onchange')
    bao_hanh = fields.Char(string='Bảo hành(tháng)', track_visibility='onchange')
    bao_hanh_toi = fields.Date(string='Bảo hành tới', track_visibility='onchange')
    chi_phi = fields.Integer(string='Chi phí sửa chữa', track_visibility='onchange')
    noi_sua = fields.Many2one('nha.cungcap',string='Nơi sửa', track_visibility='onchange')
    noi_dung_sua = fields.Text(string='Lý do sửa')



    @api.multi
    @api.depends('thoi_gian_sua')
    def get_thietbi(self):
        if self.cnect_thiet_bi:
            self.thiet_bi = self.cnect_thiet_bi.ma_thietbi
            return self.thiet_bi
        if self.cnect_xuongmay:
            self.thiet_bi = self.cnect_xuongmay.ma_so
            return self.thiet_bi

    thiet_bi = fields.Char(store=True, compute='get_thietbi', string='Thiết bị', track_visibility='onchange')


    @api.multi
    def action_nhatky_0_1(self):
        self.write({'status':'1'})
        self.thoi_gian_hoan_thanh = datetime.now()

    # tạo chỉ số chạy tự động

    @api.model
    def create(self, vals):
        if (vals.get('seq_nhatky_code', 'New') == 'New'):
            vals['so_nhat_ki'] = self.env['ir.sequence'].next_by_code('nhatky_code') or '/'
            return super(LineNhatKy, self).create(vals)