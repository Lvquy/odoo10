# -*- coding: utf-8 -*-

from odoo import api, fields, models,_

class Document(models.Model):
    _name='doc.lds'
    # _order='state ASC'

    name = fields.Char(string='Name')
    # state = fields.Integer(string='Bước')
    #
    # document= fields.Html(string='Hướng dẫn sử dụng nội bộ')