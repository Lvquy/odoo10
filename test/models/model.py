from odoo import fields, models, api


class Ban(models.Model):
    _name = 'ban'


    khach =  fields.Many2one('khach')
    name =fields.Char(string='Ten don hang')
    def confirm(self):
        self.env['khach'].search([('name','=',self.khach.name)]).dem_ban()
    def set_name(self):
        self.name = 'abc'


class Khach(models.Model):
    _name = 'khach'

    name = fields.Char(string="Ten khach hang")
    count = fields.Integer(store=True)

    def dem_ban(self):
        self.count = self.env['ban'].search_count([('khach.name','=',self.name)])
class MySetting(models.TransientModel):
    _name = 'ban.config.settings'
    _inherit = 'res.config.settings'


    default_name = fields.Char(default_model='ban')


    test_config = fields.Char()

    @api.model
    def get_default_test_config_values(self, fields):
        """
        Method argument "fields" is a list of names
        of all available fields.
        """
        ban = self.env['ban'].search([],limit=1)
        return {
            'test_config': ban.name,
            }

    @api.one
    def set_ban_values(self):
        ban = self.env['ban'].search([],limit=1)
        ban.name = self.test_config
