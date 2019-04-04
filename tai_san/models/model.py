# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-


from odoo import api, fields, models,_
from odoo.exceptions import UserError

class Taisan(models.Model):
    _name = 'tai.san'
    _description = 'Cac loai tai san'
    _rec_name = 'name'
    _inherit = 'mail.thread'

    img = fields.Binary(string='Hình ảnh')
    code = fields.Char(string='Mã thiết bị', default='New', readonly=True)
    name = fields.Char(string='Tên tài sản', track_visibility='onchange')
    gia_tri = fields.Integer(string='Giá trị', track_visibility='onchange')
    ngay_mua = fields.Date(string='Ngày mua' , track_visibility='onchange')
    bao_hanh_toi = fields.Date(string='Bảo hành tới', track_visibility='onchange')
    nguoi_bao_quan = fields.Many2one('hr.employee',string='Người bảo quản', track_visibility='onchange')
    status = fields.Selection([('0','Kho'),('1','Đang dùng'),('2','Phế')],string='Trạng thái',default='0',track_visibility='onchange')
    ngay_batdau_bao_quan = fields.Date(string="Từ khi")
    ly_do_phe = fields.Text(string='Lý do báo phế')
    ngay_bao_phe = fields.Date(string="Ngày báo phế")
    nha_cung_cap = fields.Many2one('res.partner',string='Nhà cung cấp',domain=[('supplier','=',True)])





    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('code_code') or '/'
        return super(Taisan, self).create(vals)

    @api.multi
    def confirm(self):
        if self.nguoi_bao_quan:
            self.env['hr.employee'].search([('thiet_bi.code','=',self.code)]).write({'thiet_bi': [(3, self.id)]})
            self.env['hr.employee'].search([('name','=',self.nguoi_bao_quan.name)]).write({'thiet_bi': [(4, self.id)]})
            self.write({'status': '1'})
        elif self.nguoi_bao_quan is not True:
            # self.env['hr.employee'].search([('thiet_bi.code', '=', self.code)]).write({'thiet_bi': [(3, self.id)]})
            self.write({'status': '0'})
            raise UserError (_('Cần có người bảo quản'))
    @api.multi
    def unconfirm(self):
        self.env['hr.employee'].search([('thiet_bi.code', '=', self.code)]).write({'thiet_bi': [(3, self.id)]})
        self.nguoi_bao_quan = False
        self.write({'status':'0'})
    @api.multi
    def cancel(self):
        if not self.ly_do_phe:
            raise UserError('Cần có lý do!')
        self.env['hr.employee'].search([('thiet_bi.code', '=', self.code)]).write({'thiet_bi': [(3, self.id)]})
        self.nguoi_bao_quan = False
        self.write({'status':'2'})
class HR(models.Model):
    _inherit = 'hr.employee'

    thiet_bi = fields.Many2many('tai.san','nguoi_bao_quan',string='Thiet bi', readonly=True)