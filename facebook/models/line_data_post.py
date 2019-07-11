# -*- coding: utf-8 -*-

from odoo import fields, models, api
import requests
import json


class LineDataPost(models.Model):
    _name = 'line.datapost'

    message_post = fields.Text()
    id_post = fields.Char()
    link_fb = fields.Char(default="https://facebook.com/")
    ref = fields.Many2one('get.id')

    def truyvan(self):

        id_post =  str(self.id_post)
        id_post_new = id_post.rsplit('_')[1]
        new = self.env['new.user'].search([])
        print new, 'new '
        id_post_old = []
        for i in new:
            id_post_old.append(i.id_post)
        print id_post_old

        if id_post_new not in id_post_old:
            new.create({
                'id_post': id_post_new,
                'note': self.message_post
            })