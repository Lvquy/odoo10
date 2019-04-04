# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date


class Skype(models.Model):
    _name = 'skype'
    _rec_name = 'name'

    name = fields.Char(string='User')
    passw = fields.Char(string='Password')
    nguoi_sd = fields.Many2one('nguoi.baoquan', string='Người sử dụng')

    