# -*- coding: utf-8 -*-

from odoo import fields, models, api
import requests

class FaceBook(models.Model):
    _name = 'setting.fb'

    key = fields.Char(string='Access Token')
    id_page = fields.Char(string='ID Page')
    field_get = fields.Text(string='Field get')
    active_fb = fields.Boolean(default=True, string='Active')
    message_auto_rep = fields.Text(string ='Message Auto Reply')

class ToolsGetID(models.Model):
    _name = 'get.id'

    fb_url = fields.Char()
    id_fb = fields.Char()

    def get_id_fb(self):
        URL = "https://findmyfbid.com/"
        PARAMS = {'url': self.fb_url}
        try:
            r = requests.post(url=URL, params=PARAMS)
            self.id_fb = r.json().get("id")
            return
        except Exception:
            return 0

class PageFB(models.Model):
    _name = 'page.fb'

    mesage_feed = fields.Text()

    def post_to_feed(self):
        print 'post to feed'

class NewUser(models.Model):
    _name = 'new.user'

    id_post = fields.Char()
    note =fields.Text(string='Description')
    data_get = fields.One2many('line.fb', 'cnect_cmt')
    data_get_cmt = fields.One2many('line.fb', 'cnect_like')

    def create_user_fb(self):
        print 'create fb'
        data_like = self.data_get
        data_cmt = self.data_get_cmt
        customer = self.env['res.partner']
        for i in data_like:
            print i.id_fb
            customer.create({
                'name_fb':i.name_fb,
                'link_fb':'https://facebook.com'+'/'+i.id_fb,
                'name': i.name_fb,
                'fb_id': i.id_fb,
            })

    @api.multi
    def get_data_fb(self):
        data_api = self.env['setting.fb'].search([('active_fb','=',True)], limit=1)
        key = data_api.key
        user_id = data_api.id_page
        field_get = data_api.field_get
        like = self.search([('id_post', '=', self.id_post)], limit=1)
        cmt = self.search([('id_post', '=', self.id_post)], limit=1)

        try:
            a = requests.get("https://graph.facebook.com/v3.3/" + user_id + '_' + self.id_post + '?fields=' + field_get,params={'access_token': key}).json()
            data_cmt = a.get("comments").get('data')
            for k in data_cmt:
                cmt.write({
                    'data_get_cmt': [(0, 0, {
                        'id_fb': k.get("from").get("id"),
                        'name_fb': k.get("from").get("name"),
                        'link_fb': '',
                        'action_type': 'comment',
                    })]
                })
        except Exception:
            print 'khong co cmt'
        try:
            a = requests.get("https://graph.facebook.com/v3.3/" + user_id + '_' + self.id_post + '?fields=' + field_get,params={'access_token': key}).json()
            data_like = a.get("likes").get("data")

            for k in data_like:
                like.write({
                    'data_get': [(0, 0, {
                        'id_fb': k.get("id"),
                        'name_fb': k.get("name"),
                        'link_fb': '',
                        'action_type': 'like',
                    })]
                })

        except Exception:
            print 'khong co like'
