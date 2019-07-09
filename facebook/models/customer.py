# -*- coding: utf-8 -*-

from odoo import fields, models, api
import requests

class GETFB(models.Model):
    _inherit = 'res.partner'

    name_fb = fields.Char(string='Facebook name')
    link_fb = fields.Char(string='Link FB')
    fb_id = fields.Char(string='User ID')