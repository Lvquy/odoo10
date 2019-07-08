# -*- coding: utf-8 -*-

from odoo import fields, models, api
import requests

class APIFB(models.Model):
    _name = 'api.facebook'

    api_key= fields.Char()
    fields_list = fields.Char(string='Fields list')
    cmt = fields.Char(string='cmt')

class MySetting(models.TransientModel):
    _name = 'api.facebook.config.settings'
    _inherit = 'res.config.settings'

    # default_name = fields.Char(default_model='api')
    api_key = fields.Char()

    @api.model
    def get_default_tuythich(self, fields):
        data = self.env['api.facebook'].search([],limit=1)
        return {
            'api_key': data.api_key,
            }
    @api.one
    def set_tuythich_abc(self):
        data = self.env['api.facebook'].search([],limit=1)
        data[0].api_key = self.api_key

class GETFB(models.Model):
    _inherit = 'res.partner'

    name_fb = fields.Char()
    link_fb = fields.Char()

    def get_fb(self):
        key = self.env['api.facebook'].search([],limit=1).api_key
        user_id = 'me'
        data = self.env['api.facebook'].search([])
        field = []
        field_get = ''
        for i in data:
            field.append(i.fields_list)
        for k in field:
            field_get +=k+','
        field_get = field_get.rstrip(',')

        a = requests.get("https://graph.facebook.com/v2.12/" + user_id + '?fields=' + field_get,
                         params={'access_token': key}).json()
        if a['feed']:
            c = a['feed']['data']

        for k in c:
            for p in k['likes']['data']:
                print p['name']
                print p['link']
                self.create({'name_fb':p['name'],
                            'link_fb':p['link'],
                            'name': p['name']

                            })
