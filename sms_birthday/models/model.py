# -*- coding:utf-8 -*-
from datetime import date

import dateutil.parser
from pushbullet import Pushbullet

from odoo import models, api

API_KEY ='o.08l11dgmJ0Et9LZRJei5EPUJ6onmAmfL'
pb = Pushbullet(API_KEY)
device = pb.devices[0]

class Birthday(models.Model):
    _inherit = 'hr.employee'

    def auto_sms(self):
        data = self.env['hr.employee']
        id_all = data.search([])
        # id_need = data.browse(id_all)
        # print id_need
        for i in id_all:

            day = date.today().day
            month = date.today().month
            birthday = i.birthday
            birthday_day = dateutil.parser.parse(birthday).day
            birthday_month = dateutil.parser.parse(birthday).month
            if birthday_month == month and birthday_day == day:
                id_need = data.browse(i.id)
                mobile= id_need.mobile_phone
                sms = "Chúc bạn " + str(id_need.name) + " Sinh nhật vui vẻ! " + str(birthday)
                pb.push_note('Happy Birthday!', sms)
                pb.push_sms(device, mobile, sms)