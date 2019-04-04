# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
import datetime
from odoo.exceptions import UserError

class BaoTri(models.Model):
    _name = 'baotri'
    _rec_name = 'today_1'

    today_1 = fields.Date(string='Ngày hôm nay', default = datetime.date.today())
    list_may = fields.One2many('line.baotri','cnect_baotri')
    @api.model
    def get_default_lines(self):
        list = []
        line_count = self.env['xuong.may'].search([('da_baotri','=',True)])
        print 'line count:',line_count
        for i in line_count:
            print 'i:',i
            list.append([0, 0, {'thiet_bi': i.id,
                                'status': False
                                }])
        print 'list:',list
        return list

    list_may = fields.One2many('line.baotri', 'cnect_baotri',coppy=True, default = get_default_lines)