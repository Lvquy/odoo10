# -*- coding:utf-8 -*-
from pushbullet import Pushbullet
from odoo import api, fields, models
pb = Pushbullet('o.08l11dgmJ0Et9LZRJei5EPUJ6onmAmfL')
# device = pb.devices[0]
# push = pb.push_sms(device, "+84868189506", "Wowza!")
# push = pb.push_note("This is the title", "day la tin nhan tu dong")
print(pb.channels)
my_channel = pb.channels[0]

push = my_channel.push_note("Hello Channel!", "Hello My Channel")

