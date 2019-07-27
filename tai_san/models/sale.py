# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import UserError
from datetime import date
import num2text


class Sale(models.Model):
    _name = 'ban.phelieu'

    khach_hang = fields.Many2one('res.partner', string='Khách hàng')
    ngay_tao = fields.Date(string='Ngày tạo', default= date.today())
    ngay_xuat_kho = fields.Date(string='Ngày xuất kho')
    tai_san_ban = fields.One2many('line.taisan','ref_ban',string='Tài sản bán', required=True)
    note = fields.Text(string='Ghi chú')
    status = fields.Selection([('0','Bản thảo'),('1','Đã bán'),('2','Hủy')], string='Trạng thái SO', default='0')
    tong_tien = fields.Float(string='Tổng tiền(VND)',store=True, compute='get_tong', default=0)
    so = fields.Char(string='Số đơn hàng', readonly=True)
    doc_tien = fields.Char(string='Đọc tiền', compute='get_doc_tien')


    @api.model
    def create(self, vals):
        vals['so'] = self.env['ir.sequence'].next_by_code('code_so') or '/'
        return super(Sale, self).create(vals)


    @api.one
    @api.depends('tai_san_ban')
    def get_tong(self):
        data = self.tai_san_ban
        for i in data:
            self.tong_tien += i.tong

    # @api.one
    @api.multi
    def confirm_sale(self):
        if self.ngay_xuat_kho:
            self.status='1'
            data = self.tai_san_ban
            for i in data:
                i.ts.khach_hang = self.khach_hang
                print i.ts.name
                i.ts.da_ban = True
                i.ts.write({
                'lich_su_bao_quan': [(0, 0, {
                    'his_type': 'ban_phe_lieu',
                    'note': '',
                    'nguoi_bq': self.khach_hang.name,
                    'so_the': '',
                    'thiet_bi': i.ts.name,
                    'tu_ngay': date.today()
            })]

                })
        else:
            raise UserError('Cần có ngày xuất kho!')

    def cancel_sale(self):
        self.status='2'

    @api.multi
    def unlink(self):
        if self.status in ('1'):
            raise UserError('Không được xóa đơn hàng đã hoàn thành!')
        else:
            return super(Sale, self).unlink()

    @api.onchange('tong_tien')
    def get_doc_tien(self):
        self.doc_tien = num2text.docso(int(self.tong_tien))
        # print self.doc_tien


class Linets(models.Model):
    _name = 'line.taisan'

    ref_ban = fields.Many2one('ban.phelieu',required=True)
    ts = fields.Many2one('tai.san',string='Tài sản', required=True)
    mats = fields.Char(related='ts.code',string='Mã TS')
    sl = fields.Float(string='S.Lượng', default=1)
    dvt = fields.Char(string='ĐVT')
    dg = fields.Float(string='Đ.Giá(VND)')
    tong = fields.Float(string='Tổng tiền(VND)', store=True, compute='compute_tong')

    @api.one
    @api.depends('sl','dg')
    def compute_tong(self):
        self.tong = self.sl*self.dg



