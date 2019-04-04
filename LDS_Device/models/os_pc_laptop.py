# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Os(models.Model):
    _name = 'os'
    _rec_name = 'name'

    name = fields.Char(string='Tên hệ thống')