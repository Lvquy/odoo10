# -*- coding: utf-8 -*-
from odoo import fields, models, api

class LineCheck(models.Model):
    _name = 'line.check'

    cnect_logcheck = fields.Many2one('log.check', string='Kiểm tra camera')
    check = fields.Boolean(default=False, string='Bị hỏng?')
    error = fields.Text('Mô tả lỗi')

    line_check = fields.Many2one('thietbi', string='Thiết bị')
    vi_tri = fields.Char(string='Vị trí')
