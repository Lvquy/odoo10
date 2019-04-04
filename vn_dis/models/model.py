# -*- coding: utf-8 -*-

import json
from odoo import api, fields, models,_
# -*- coding: utf-8 -*-

from pushbullet import Pushbullet
pb = Pushbullet('o.Et4pxH6uDRH0s0RHaUp9mpazs0vHX7rZ')
device = pb.devices[0]
# push = pb.push_sms(device, "+84868189506", "Đây là tin nhắn tự động")

class Tinh(models.Model):
    _name = 'tinh'

    name = fields.Char(string='Tên tỉnh')
    code_tinh = fields.Char(string='Mã tỉnh')

    def test(self):
        return pb.push_note("Odoo LDS", "Đây là thông báo tự động ")

class Huyen(models.Model):
    _name = 'huyen'

    name = fields.Char(string='Tên huyện')
    code_huyen = fields.Char(string='Mã Huyện')
    parent_code = fields.Char(string="Mã tỉnh")
    thuoc_tinh = fields.Many2one('tinh', string='Thuộc tỉnh')



class Xa(models.Model):
    _name ='xa'

    name = fields.Char(string='Tên xã')
    code_xa = fields.Char(string="Mã xã")
    parent_code = fields.Char(string='Mã huyện')
    thuoc_huyen = fields.Many2one('huyen',string='Thuộc huyện')
    thuoc_tinh = fields.Many2one(related='thuoc_huyen.thuoc_tinh',string='Thuộc tỉnh', readonly=True)

class Khach(models.Model):
    _inherit = 'res.partner'

    tinh = fields.Many2one('tinh',string='Tỉnh')
    xa = fields.Many2one('xa',string='Xã')
    huyen = fields.Many2one('huyen', string='Huyện')
    so_nha = fields.Char(string='Số nhà, tên đường')



    @api.onchange('tinh')
    def onchange_tinh(self):
        res = {}
        self.huyen = False
        parent_code =''
        if self.tinh:
            list_huyen = self.env['huyen'].search([('parent_code','=',self.tinh.code_tinh)])
            if  len(list_huyen) >0:
                parent_code= list_huyen[0].parent_code
            res = {'domain': {'huyen': [('parent_code','=',parent_code)]}}
        else:
            res ={}
        return res

    @api.onchange('huyen')
    def onchange_huyen(self):
        res = {}
        self.xa = False
        parent_code=''
        if self.huyen:
            list_xa = self.env['xa'].search([('parent_code', '=', self.huyen.code_huyen)])
            if len(list_xa)>0:
                parent_code = list_xa[0].parent_code
            res = {'domain': {'xa': [('parent_code', '=', parent_code)]}}
        return res
