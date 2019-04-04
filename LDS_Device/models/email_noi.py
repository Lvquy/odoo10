# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date


class EmailNoi(models.Model):
    _name = 'email.noi'
    _rec_name = 'name'

    name = fields.Char(string='User')
    passw = fields.Char(string='Password')
    nguoi_sd = fields.Many2one('nguoi.baoquan', string='Người sử dụng')

    @api.multi
    def print_email_noi(self):
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'LDS_Device.report_email_noibo_1'
        }