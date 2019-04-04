# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
class LineThietBi(models.Model):
    _name = 'line.thietbi'
    _rec_name = 'thiet_bi'
    _inherit = 'mail.thread'

    cnect_nguoi_bao_quan = fields.Many2one('nguoi.baoquan', track_visibility='onchange')
    thiet_bi = fields.Many2one('thietbi', string='Thiết bị', track_visibility='onchange')
    ngay_bao_quan = fields.Date(string='Ngày bắt đầu bảo quản', track_visibility='onchange')
    ngay_tra = fields.Date(string='Ngày trả', track_visibility='onchange')

    @api.multi
    def action_tra(self):
        self.write({'ngay_tra': datetime.now()})