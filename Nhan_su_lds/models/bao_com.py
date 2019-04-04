# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime, time
import dateutil.parser
from odoo.exceptions import UserError,ValidationError
from lxml import etree


class BaoCom(models.Model):
    _name = 'bao.com'
    _rec_name = 'bo_phan'
    _order = 'gio_bao desc'

    gio_bao = fields.Datetime(string='Giờ báo', default=datetime.datetime.now(), readonly=True)
    ngay_bao = fields.Date(string='Ngày báo', default=lambda s: datetime.date.today())
    nguoi_bao = fields.Many2one('res.users', string='Người báo', readonly=True, default=lambda self: self.env.user)
    bo_phan = fields.Char(store=True, compute='get_bo_phan', string='Bộ phận', readonly=True)

    com_man_trua = fields.Integer(string='Cơm mặn trưa')
    com_chay_trua = fields.Integer(string='Cơm chay trưa')
    chao_trua = fields.Integer(string='Cháo trưa')


    man_4_chieu =fields.Integer(string='Mặn 4T')
    chay_4_chieu =fields.Integer(string='Chay 4T')
    chao_4_chieu =fields.Integer(string='Cháo 4T')

    man_3_chieu = fields.Integer(string='Mặn 3T')
    chay_3_chieu = fields.Integer(string='Chay 3T')
    chao_3_chieu = fields.Integer(string='Cháo 3T')

    bun = fields.Integer(string='Bún chiều')
    mi = fields.Integer(string='Mì chiều')

    com_buoi = fields.Selection([('trua', 'Cơm trưa'), ('chieu', 'Cơm chiều')], required=True, string='Buổi')
    note = fields.Text(string='Ghi chú')
    bao_thay = fields.Selection([
        ('TMAY', 'Tổ máy'),
        ('CNC', 'CNC'),
        ('CN1', 'C.Nhám 1'),
        ('CN2', 'C.Nhám 2'),
        ('MAU', 'Mẫu'),
        ('VECNI', 'Vecni'),
        ('LRAP', 'Lắp ráp'),
        ('CTRINH', 'C.Trình'),
        ('TDO', 'T.Độ'),
        ('KHO', 'Kho'),
        ('QC', 'QC'),
        ('BTRI', 'Bảo trì'),
        ('IT', 'IT'),
    ], string='Báo thay cho')


    @api.multi
    def return_page(self):
        return {
            'type': 'ir.actions.act_url',
            'name': "Web báo cơm",
            'target': 'self',
            'url': '/page/services/'
        }

    # chỉ cho group nhân sự có quyền tạo mới ở tree and from
    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(BaoCom, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if view_type != 'search' and self.env.uid != 1:
            # Check if user is in group that allow creation
            has_my_group = self.env.user.has_group('Nhan_su_lds.group_ns')
            if not has_my_group:
                root = etree.fromstring(res['arch'])
                root.set('create', 'false')
                res['arch'] = etree.tostring(root)

        return res

    @api.onchange('com_buoi')
    def onchange_com_buoi(self):
        if self.com_buoi == 'trua':
            self.man_4_chieu = self.chay_4_chieu = self.chao_4_chieu = \
                self.man_3_chieu = self.chay_3_chieu = self.chao_3_chieu =self.bun = self.mi =0
        if self.com_buoi == 'chieu':
            self.com_man_trua = self.com_chay_trua = self.chao_trua = 0

    @api.depends('bao_thay')
    def get_bo_phan(self):
        if self.bao_thay == False:
            self.bo_phan = self.nguoi_bao.bo_phan
        else:
            self.bo_phan = self.bao_thay