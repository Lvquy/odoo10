# -*- coding: utf-8 -*-
from odoo import fields, models, api


class EmployeeAdd(models.Model):
    _inherit= 'hr.employee'

    tinh = fields.Many2one('tinh',string="Tỉnh TP")
    huyen = fields.Many2one('huyen', string="Quận Huyện")
    xa = fields.Many2one('xa', string="Xã Phường")
    duong_sonha = fields.Char(string='Tên đường, số nhà...')
    @api.onchange('tinh')
    def onchange_tinh(self):
        res = {}
        self.huyen = False
        parent_code = ''
        if self.tinh:
            list_huyen = self.env['huyen'].search([('parent_code', '=', self.tinh.code_tinh)])
            if len(list_huyen) > 0:
                parent_code = list_huyen[0].parent_code
            res = {'domain': {'huyen': [('parent_code', '=', parent_code)]}}
        else:
            res = {}
        return res

    @api.onchange('huyen')
    def onchange_huyen(self):
        res = {}
        self.xa = False
        parent_code = ''
        if self.huyen:
            list_xa = self.env['xa'].search([('parent_code', '=', self.huyen.code_huyen)])
            if len(list_xa) > 0:
                parent_code = list_xa[0].parent_code
            res = {'domain': {'xa': [('parent_code', '=', parent_code)]}}
        return res