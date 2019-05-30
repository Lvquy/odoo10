from odoo import fields, models, api


class Ban(models.Model):
    _name = 'ban'


    khach =  fields.Many2one('khach')
    name =fields.Char(string='Ten don hang')

    def confirm(self):
        self.env['khach'].search([('name','=',self.khach.name)]).dem_ban()


class Khach(models.Model):
    _name = 'khach'

    name = fields.Char(string="Ten khach hang")
    count = fields.Integer(store=True)

    def dem_ban(self):
        self.count = self.env['ban'].search_count([('khach.name','=',self.name)])