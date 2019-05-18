# -*- coding: utf-8 -*-

from odoo import api, fields, models,_



class Document(models.Model):
    _name='doc.lds'

    name = fields.Char(string='Name')
    document= fields.Html(string='Hướng dẫn sử dụng nội bộ')