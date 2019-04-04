# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ThuocTinh(models.Model):
    _name = 'thuoctinh'
    _rec_name = 'name'

    name = fields.Char(string='Kiểu thuộc tính')
    value = fields.Char(string='Giá trị thuộc tính')