# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TaiKhoan(models.Model):
    _name = 'taikhoan'
    _rec_name = 'user'
    _inherit = 'mail.thread'

    user = fields.Char(string='User', track_visibility='onchange')
    passw = fields.Char(string='Password', track_visibility='onchange')
    type = fields.Selection([('super','Supervisor'),
                             ('pow','Power user'),
                             ('normal','Normal'),
                             ('guest','Guest')], track_visibility='onchange')
