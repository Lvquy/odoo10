# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date

class NguoiBaoQuan(models.Model):
    _name = 'nguoi.baoquan'
    _rec_name = 'name'
    _inherit = 'mail.thread'

    name = fields.Char(string='Tên')
    so_the = fields.Char(string='Số thẻ')
    bo_phan = fields.Many2one('bophan', string='Bộ phận', track_visibility='onchange')
    user_mail_noi = fields.Many2one('email.noi',string='Mail nội bộ', track_visibility='onechange')
    user_mail_ngoai = fields.Many2one('email.ngoai',string='Mail ngoại bộ', track_visibility='onechange')
    user_server = fields.Many2one('server',string='User server', track_visibility='onechange')
    note = fields.Text(string='Ghi chú')
    cac_thiet_bi_bq = fields.One2many('line.thietbi','cnect_nguoi_bao_quan',string='Các thiết bị bảo quản')
    skype = fields.Many2one('skype',string='Skype')
    passw_skype = fields.Char(string='Password')