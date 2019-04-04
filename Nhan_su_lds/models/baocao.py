# -*- coding: utf-8 -*-
from odoo import http
import datetime, time
import dateutil.parser
from odoo.exceptions import UserError
from odoo import models, fields, api
import num2text



class BaoCao(models.Model):
    _name = 'bao.cao'
    _order = 'ngay_baocao desc'


    from_date = fields.Date(string='Từ ngày')
    to_date = fields.Date(string='Tới ngày', default=datetime.date.today())

    total_man_4 = fields.Integer(string='Tổng xuất mặn 4t', readonly=True)
    total_chay_4 = fields.Integer(string='Tổng xuất chay 4t', readonly=True)
    total_chao_4 = fields.Integer(string='Tổng xuất cháo 4t', readonly=True)

    total_man_3 = fields.Integer(string='Tổng xuất mặn 3t', readonly=True)
    total_chay_3 = fields.Integer(string='Tổng xuất chay 3t', readonly=True)
    total_chao_3 = fields.Integer(string='Tổng xuất cháo 3t', readonly=True)

    total_bun = fields.Integer(string='Tổng xuất bún', readonly=True)
    total_mi = fields.Integer(string='Tổng xuất mì', readonly=True)
    total_dacbiet = fields.Integer(string='Tổng xuất đặc biệt', readonly=True)
    price_total_dacbiet = fields.Integer(string='Tổng tiền xuất đặc biệt', readonly=True)

    ngay_baocao = fields.Datetime(string='Ngày báo cáo', default= datetime.datetime.now(), readonly=True)

    price_total_chay_4 = fields.Integer(string='Tổng tiền chay 4t', default=0, readonly=True)
    price_total_man_4 = fields.Integer(string='Tổng tiền mặn 4t', default=0, readonly=True)
    price_total_chao_4 = fields.Integer(string='Tổng tiền cháo 4t', default=0, readonly=True)
    price_total_4 = fields.Integer(string='Tổng tiền 4t', default=0, readonly=True)

    price_total_chay_3 = fields.Integer(string='Tổng tiền chay 3t', default=0, readonly=True)
    price_total_man_3 = fields.Integer(string='Tổng tiền mặn 3t', default=0, readonly=True)
    price_total_chao_3 = fields.Integer(string='Tổng tiền cháo 3t', default=0, readonly=True)
    price_total_3 = fields.Integer(string='Tổng tiền 3t', default=0, readonly=True)

    price_total_bun = fields.Integer(string='Tổng tiền bún', default=0, readonly=True)
    price_total_2 = fields.Integer(string='Tổng tiền 2t', default=0, readonly=True)


    total = fields.Integer('Tổng tiền', readonly=True, store=True)
    doc_tien = fields.Char('Số tiền bằng chữ',store=True, compute='_doc_tien')
    status = fields.Selection([('0', 'Bản thảo'), ('1', 'Đã khóa')], default='0')



    # @api.multi
    # def get_data(self):
    #     data = self.env['bao.com'].search([('ngay_bao','>=', self.from_day),('ngay_bao','<=',self.to_day)])
    #     for i in data:
    #         self.ngay = i.ngay_bao
    #         self.h2 = i.chao_chieu + i.bun + i.mi
    #         self.h4 = i.com_chay_trua + i.com_chay_chieu + i.com_man_trua +i.com_man_chieu + i.chao_trua
    #         self.bo_phan = i.bo_phan
    @api.multi
    def lock(self):
        self.status = '1'
        self.get_total()

    @api.multi
    def unlock(self):
        self.status = '0'

    @api.depends('total')
    def _doc_tien(self):
        self.doc_tien = num2text.docso(self.total) + u' đồng'


    @api.multi
    def get_total(self):

        self.total_man_4 = self.total_chay_4 = self.total_chao_4 = self.total_chao_3 = self.total_man_3 = self.total_chay_3 = self.total_bun = self.total_mi =\
            self.price_total_chay_4 =self.price_total_man_4= self.price_total_chao_4=self.price_total_chay_3=self.price_total_man_3=self.price_total_chao_3=\
            self.price_total_bun=self.total=self.total_dacbiet=self.price_total_dacbiet=self.price_total_4=self.price_total_3=self.price_total_2=0
        if self.to_date < self.from_date:
            raise UserError('Khoảng ngày không hợp lệ!')
        self.ngay_baocao = datetime.datetime.now()
        data = self.env['nhan.su'].search([('ngay_bao','>=',self.from_date),('ngay_bao','<=', self.to_date),('status','=','1')])
        for i in data:
            self.total_man_4 += i.today_total_man_4
            self.total_chay_4 += i.today_total_chay_4
            self.total_chao_4 += i.today_total_chao_4

            self.total_man_3 += i.today_total_man_3
            self.total_chay_3 += i.today_total_chay_3
            self.total_chao_3 += i.today_total_chao_3

            self.total_bun += i.today_total_bun
            self.total_mi += i.today_total_mi

            self.price_total_man_4 += i.money_man_4
            self.price_total_chay_4 += i.money_chay_4
            self.price_total_chao_4 += i.money_chao_4

            self.price_total_man_3 += i.money_man_3
            self.price_total_chay_3 += i.money_chay_3
            self.price_total_chao_3 += i.money_chao_3

            self.price_total_bun += i.money_bun

            self.total_dacbiet += i.total_dac_biet
            self.price_total_dacbiet +=i.money_dacbiet


            self.price_total_4 = self.price_total_man_4 + self.price_total_chay_4 +self.price_total_chao_4
            self.price_total_3 = self.price_total_man_3 + self.price_total_chay_3 +self.price_total_chao_3
            self.price_total_2 = self.price_total_bun

            self.total = self.price_total_4 +self.price_total_3+self.price_total_2+ self.price_total_dacbiet

    @api.multi
    def unlink(self):
        for i in self:
            if i.status == '1':
                raise UserError('bạn không thể xóa khi đã khóa!')
        return super(BaoCao, self).unlink()