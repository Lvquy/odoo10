# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError

class BaoCao(models.Model):
    _name = 'bao.cao'
    _order = 'id desc'

    ngay = fields.Date(string='Ngày báo cáo', default=datetime.today())

    tong_thietbi = fields.Integer(string='Tổng thiết bị',store=True, compute='depends_thietbi')
    tong_hop = fields.One2many('line.baocao','cnect_baocao', string='Tổng hợp')

    it = fields.Integer(string='IT', store=True, compute='depends_thietbi')
    kho = fields.Integer(string='Kho', store=True, compute='depends_thietbi')
    lr = fields.Integer(string='Lắp ráp', store=True, compute='depends_thietbi')
    qc = fields.Integer(string='QC', store=True, compute='depends_thietbi')
    ns = fields.Integer(string='Nhân sự', store=True, compute='depends_thietbi')
    tk = fields.Integer(string='Thiết kế', store=True, compute='depends_thietbi')
    nv = fields.Integer(string='Nghiệp vụ', store=True, compute='depends_thietbi')
    tm = fields.Integer(string='Thu mua', store=True, compute='depends_thietbi')
    xnk = fields.Integer(string='XNK', store=True, compute='depends_thietbi')
    kt = fields.Integer(string='Kế toán', store=True, compute='depends_thietbi')
    phason = fields.Integer(string='Pha sơn', store=True, compute='depends_thietbi')
    cnc = fields.Integer(string='CNC', store=True, compute='depends_thietbi')
    tdo = fields.Integer(string='Tiến độ', store=True, compute='depends_thietbi')
    sx = fields.Integer(string='Sản xuất', store=True, compute='depends_thietbi')

    @api.depends('tong_hop')
    def depends_thietbi(self):
        for i in self.tong_hop:
            self.tong_thietbi += 1
            if i.bo_phan == 'IT':
                self.it += 1
            if i.bo_phan == 'Kho':
                self.kho += 1
            if i.bo_phan == 'Lắp ráp':
                self.lr += 1
            if i.bo_phan == 'QC':
                self.qc += 1
            if i.bo_phan == 'Nhân sự':
                self.ns += 1
            if i.bo_phan == 'Thiết kế':
                self.tk += 1
            if i.bo_phan == 'Nghiệp vụ':
                self.nv += 1
            if i.bo_phan == 'Thu mua':
                self.tm += 1
            if i.bo_phan == 'XNK':
                self.xnk += 1
            if i.bo_phan == 'Kế toán':
                self.kt += 1
            if i.bo_phan == 'Pha sơn':
                self.phason += 1
            if i.bo_phan == 'CNC':
                self.cnc += 1
            if i.bo_phan == 'Tiến độ':
                self.tdo += 1
            if i.bo_phan == 'Sản xuất':
                self.sx += 1

    class Linebc(models.Model):
        _name = 'line.baocao'
        _order = 'bo_phan desc'

        thiet_bi = fields.Many2one('thietbi', string='Thiết bị')
        nguoi_bq = fields.Char(related='thiet_bi.nguoi_bao_quan.name', string='Người bảo quản')
        kieu_thietbi = fields.Char(related='thiet_bi.model_thiet_bi')
        bo_phan = fields.Char(related='thiet_bi.nguoi_bao_quan.bo_phan.name', string='Bộ phận')
        cnect_baocao = fields.Many2one('bao.cao',string='Kết nối')
