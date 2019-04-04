# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BoPhan(models.Model):
    _name = 'bophan'
    _rec_name = 'name'

    name = fields.Char(string='Tên bộ phận')