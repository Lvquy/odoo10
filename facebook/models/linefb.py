# -*- coding: utf-8 -*-
from odoo import fields, models, api

class LineFB(models.Model):
    _name = 'line.fb'

    status = fields.Selection([('new','new'),('seen','seen')],default='new')
    id_fb = fields.Char()
    name_fb = fields.Char()
    link_fb = fields.Char()
    rep_cmt = fields.Char()
    action_type = fields.Selection([('like','like'),('comment','comment')])
    cnect_cmt = fields.Many2one('new.user',domain="[('action_type','=','comment')]")
    cnect_like = fields.Many2one('new.user' ,domain="[('action_type','=','like')]")

    def rep_cmt(self):
        print 'rep cmt'
        return
    def delete_cmt(self):
        print 'delete cmt'
        return

    def create_sale_order(self):
        print 'create sale order'

    @api.multi
    def change_status(self):
        if self.status=='new':
            self.status = 'seen'
        else:
            self.status = 'new'

