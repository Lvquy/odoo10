# -*- coding: utf-8 -*-

from odoo import fields, models, api
import requests
import json
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
    id_fb = fields.Char(readonly=True)
    type_get = fields.Selection([('id_post','Get ID Post'),('id_user_page','Get ID User, Page')],default='id_post')
    id_page = fields.Char(default=lambda self: self.env['setting.fb'].search([('active_fb','=',True)],limit=1).id_page)
    limit_post= fields.Integer(default=5)
    data_post = fields.One2many('line.datapost', 'ref', string='Data Post')
    name = fields.Char()

    def get_id_fb(self):
        if self.type_get =='id_user_page':
            URL = "https://findmyfbid.com/"
            PARAMS = {'url': self.fb_url}
            try:
                r = requests.post(url=URL, params=PARAMS)
                self.id_fb = r.json().get("id")
                return
            except Exception:
                return 0
    @api.multi
    def get_id_post(self):
        if self.type_get == 'id_post':
            graph_api_url = 'https://graph.facebook.com/v3.3/'+self.id_page+"/feed"+'?limit='+str(self.limit_post)
            params={'access_token': self.env['setting.fb'].search([('active_fb','=',True)],limit=1).key}
            try:
                data = requests.get(graph_api_url,params=params).json()
                bb = data.get("data")
            except Exception:
                return 0
            data_id_old = []
            for i in self.data_post:
                data_id_old.append(i.id_post)
            for i in bb:
                if i.get('id') not in data_id_old:
                    self.search([]).write({
                        'data_post': [(0, 0, {
                            'message_post': i.get('message'),
                            'id_post': i.get('id'),
                            'link_fb': 'https://facebook.com/'+i.get('id'),
                        })]
                    })
class PageFB(models.Model):
    _name = 'page.fb'

    mesage_feed = fields.Text()

    def post_to_feed(self):
        print 'post to feed'

class NewUser(models.Model):
    _name = 'new.user'

    id_post = fields.Char(required=True)
    note =fields.Text(string='Description')
    data_get = fields.One2many('line.fb', 'cnect_cmt')
    data_get_cmt = fields.One2many('line.fb', 'cnect_like')

    def create_user_fb(self):
        print 'create customer from data fb'
        data_like = self.data_get
        data_cmt = self.data_get_cmt


        customer = self.env['res.partner']
        data_id_customer_old = []

        for i in customer.search([('active','=',True)]):
            data_id_customer_old.append(i.fb_id)

        for i in data_like:
            if i.id_fb not in data_id_customer_old:
                customer.create({
                    'name_fb':i.name_fb,
                    'link_fb':'https://facebook.com'+'/'+i.id_fb,
                    'name': i.name_fb,
                    'fb_id': i.id_fb,
                    'custommer': True,
                })


        for i in data_cmt:
            if i.id_fb not in data_id_customer_old:
                customer.create({
                    'name_fb':i.name_fb,
                    'link_fb':'https://facebook.com'+'/'+i.id_fb,
                    'name': i.name_fb,
                    'fb_id': i.id_fb,
                })

    def get_data_fb(self):
        data_api = self.env['setting.fb'].search([('active_fb','=',True)], limit=1)
        key = data_api.key
        user_id = data_api.id_page
        field_get = data_api.field_get
        like = self.search([('id_post', '=', self.id_post)], limit=1)
        cmt = self.search([('id_post', '=', self.id_post)], limit=1)
        a = requests.get("https://graph.facebook.com/v3.3/" + user_id + '_' + self.id_post + '?fields=' + field_get,
                         params={'access_token': key}).json()
        try:
            data_cmt_get = a.get("comments").get('data')
        except Exception:
            data_cmt_get =  {}

        data_cmt_old = []
        data_cmt_new = []
        for i in self.data_get_cmt:
            data_cmt_old.append(i.id_fb)

        for i in data_cmt_get:
            data_cmt_new.append(i.get('from').get('id'))

        for i in data_cmt_old:
            if i in data_cmt_new:
                del data_cmt_new[data_cmt_new.index(i)]
                print 'trung: ', i
        for k in data_cmt_get:
            if k.get("from").get("id") in data_cmt_new:
                cmt.write({
                    'data_get_cmt': [(0, 0, {
                        'id_fb': k.get("from").get("id"),
                        'name_fb': k.get("from").get("name"),
                        'link_fb': '',
                        'action_type': 'comment',
                        'msg': k.get("message"),
                    })]
                })
        # end cmt *********************************************************
        try:
            data_like_get = a.get("likes").get('data')
        except Exception:
            data_like_get = {}

        data_like_new = []
        data_like_old = []

        for i in self.data_get:
            data_like_old.append(i.id_fb)

        for i in data_like_get:
            data_like_new.append(i.get('id'))

        for i in data_like_old:
            if i in data_like_new:
                del data_like_new[data_like_new.index(i)]
                print 'trung: ', i

        for k in data_like_get:
            if k.get("id") in data_like_new:
                like.write({
                    'data_get': [(0, 0, {
                        'id_fb': k.get("id"),
                        'name_fb': k.get("name"),
                        'link_fb': '',
                        'action_type': 'like',
                    })]
                })

        # ****************
