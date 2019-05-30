# -*- coding: utf-8 -*-

from odoo import api, fields, models,_

class Tinh(models.Model):
    _name = 'tinh'

    name = fields.Char(string='Tên tỉnh', required=True)
    code_tinh = fields.Char(string='Mã tỉnh' , required=True)

class Huyen(models.Model):
    _name = 'huyen'

    name = fields.Char(string='Tên huyện', required=True)
    code_huyen = fields.Char(string='Mã Huyện', required=True)
    parent_code = fields.Char(string="Mã tỉnh", required=True)
    thuoc_tinh = fields.Many2one('tinh', string='Thuộc tỉnh', required=True)

class Xa(models.Model):
    _name ='xa'

    name = fields.Char(string='Tên xã', required=True)
    code_xa = fields.Char(string="Mã xã", required=True)
    parent_code = fields.Char(string='Mã huyện', required=True)
    thuoc_huyen = fields.Many2one('huyen',string='Thuộc huyện', required=True)
    thuoc_tinh = fields.Many2one(related='thuoc_huyen.thuoc_tinh',string='Thuộc tỉnh', readonly=True, required=True)