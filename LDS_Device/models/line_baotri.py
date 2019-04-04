# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import UserError

class LineBaotri(models.Model):
    _name = 'line.baotri'
    _rec_name = 'thiet_bi'

    thiet_bi = fields.Many2one('xuong.may', string='Thiết bị')
    status = fields.Boolean(string='Đã bảo trì', default=False)
    ngay_bao_tri = fields.Date(realted='thiet_bi.ngay_baotri', string='Ngày bảo trì')
    cnect_baotri = fields.Many2one('baotri')
