# -*- coding: utf-8 -*-
from odoo import http
import datetime, time
import dateutil.parser
from odoo.exceptions import UserError
from odoo import models,exceptions, fields, api,_
import num2text
from odoo import api, fields, models, _


class Nhansu(models.Model):
    _name = 'nhan.su'
    _order = 'ngay_bao desc'


    # com_buoi = fields.Selection([('trua','Trưa'),('chieu','Chiều')],string='Cơm buổi')
    ngay_bao = fields.Date(string='Ngày', default= datetime.date.today())

    price_man_4 = fields.Integer(string='Giá tiền',readonly=True)
    price_chay_4 = fields.Integer(string='Giá tiền',readonly=True)
    price_chao_4 = fields.Integer(string='Giá tiền',readonly=True)
    price_man_3 = fields.Integer(string='Giá tiền',readonly=True)
    price_chay_3 = fields.Integer(string='Giá tiền',readonly=True)
    price_chao_3 = fields.Integer(string='Giá tiền',readonly=True)
    price_bun = fields.Integer(string='Giá tiền',readonly=True)

    man_trua = fields.Integer(string='Cơm mặn trưa',readonly=True)
    chay_trua = fields.Integer(string='Cơm chay trưa',readonly=True)
    chao_trua = fields.Integer(string='Cháo trưa',readonly=True)

    img_man_trua = fields.Binary(string='Ảnh món mặn')
    img_chay_trua = fields.Binary(string='Ảnh món chay')

    note= fields.Text(string='Ghi chú')
    note_chieu= fields.Text(string='Ghi chú')
    status= fields.Selection([('0','Bản thảo'),('1','Đã xong')],default='0', string='Trạng thái')

    # Tăng ca 4 tiếng
    man_4_chieu = fields.Integer(readonly=True)
    chay_4_chieu = fields.Integer(readonly=True)
    chao_4_chieu = fields.Integer(readonly=True)

    # Tăng ca 3 tiếng
    man_3_chieu = fields.Integer(readonly=True)
    chay_3_chieu = fields.Integer(readonly=True)
    chao_3_chieu = fields.Integer(readonly=True)

    # Tăng ca 2 tiếng
    bun_chieu = fields.Integer(readonly=True)
    mi_chieu = fields.Integer(readonly=True)

    #phần ăn đặc biệt
    dac_biet = fields.Integer(string='Phần đặc biệt')
    total_dac_biet = fields.Integer(string='Phần đặc biệt',related='dac_biet', readonly=True)
    price_dacbiet = fields.Integer(string='Giá tiền',readonly=True)
    money_dacbiet = fields.Integer(string='Thành tiền',readonly=True)

    img_man_chieu = fields.Binary()
    img_chay_chieu = fields.Binary()

    today_total_man_4 = fields.Integer(string='Tổng mặn 4t', readonly=True)
    today_total_chay_4 = fields.Integer(string='Tổng chay 4t', readonly=True)
    today_total_chao_4 = fields.Integer(string='Tổng cháo 4t', readonly=True)

    today_total_man_3 = fields.Integer(string='Tổng mặn 3t', readonly=True)
    today_total_chay_3 = fields.Integer(string='Tổng chay 3t', readonly=True)
    today_total_chao_3 = fields.Integer(string='Tổng cháo 3t', readonly=True)

    today_total_bun = fields.Integer(string='Tổng bún', readonly=True)
    today_total_mi = fields.Integer(string='Tổng mì', readonly=True)
    count_baocao = fields.Integer(store=True, compute='check_ngay')

    money_man_4 = fields.Integer(string="Tiền mặn 4t", readonly=True)
    money_chay_4 = fields.Integer(string="Tiền chay 4t", readonly=True)
    money_chao_4 = fields.Integer(string="Tiền cháo 4t", readonly=True)

    money_man_3 = fields.Integer(string="Tiền mặn 3t", readonly=True)
    money_chay_3 = fields.Integer(string="Tiền chay 3t", readonly=True)
    money_chao_3 = fields.Integer(string="Tiền cháo 3t", readonly=True)
    money_bun = fields.Integer(string="Tiền bún", readonly=True)

    total_today = fields.Integer(string='Tổng tiền', readonly=True)
    doc_tien = fields.Char(string='Đọc tiền', store=True, compute="_doc_tien")

    @api.depends('total_today')
    def _doc_tien(self):
        self.doc_tien = num2text.docso(self.total_today) + u' đồng'

    # check ngay_bao
    @api.one
    @api.depends('ngay_bao')
    def check_ngay(self):
        for i in self:
            i.count_baocao = self.env['nhan.su'].search_count([('status', '=', '1')])
        for x in range(self.count_baocao):
            if self.ngay_bao == self.env['nhan.su'].search([('status', '=', '1')])[x].ngay_bao:
                raise UserError('Đã tồn tại báo cơm cho ngày này')

    @api.multi
    def lock(self):
        self.check_ngay()
        self.get_total()
        self.status = '1'
    @api.multi
    def unlock(self):
        self.status = '0'
    def _test(self,ngay_bao):
        self.env.cr.execute('SELECT bo_phan,id FROM bao_com WHERE ngay_bao=%r'%(ngay_bao))
        for i in self.env.cr.fetchall():
            print i
            for j in i:
                print j



        # context = self._context
        #
        # current_uid = context.get('uid')
        #
        # user = self.env['res.users'].browse(current_uid)
        # print user.name


    @api.multi
    def get_total(self):
        self._test('2019-01-23')
        data_trua = self.env['bao.com'].search([('ngay_bao','=', self.ngay_bao),('com_buoi','=','trua')])
        data_chieu = self.env['bao.com'].search([('ngay_bao','=',self.ngay_bao),('com_buoi','=','chieu')])
        self.man_trua = self.chay_trua = self.chao_trua = 0

        price_list = self.env['setting'].search([])
        for p in price_list:
            self.price_man_4 = p.man_4
            self.price_chay_4 = p.chay_4
            self.price_chao_4 = p.chao_4
            self.price_chao_3 = p.chao_3
            self.price_chay_3 = p.chay_3
            self.price_man_3 = p.man_3
            self.price_bun = p.bun
            self.price_dacbiet = p.dac_biet

        for i in data_trua:
            self.man_trua += i.com_man_trua
            self.chay_trua += i.com_chay_trua
            self.chao_trua += i.chao_trua
        # lats xem lai
        self.man_4_chieu = self.chay_4_chieu = self.chao_4_chieu = self.man_3_chieu = \
            self.chay_3_chieu = self.chao_3_chieu= self.bun_chieu =self.mi_chieu =0
        for j in data_chieu:

            self.man_4_chieu +=j.man_4_chieu
            self.chay_4_chieu +=j.chay_4_chieu
            self.chao_4_chieu +=j.chao_4_chieu

            self.man_3_chieu +=j.man_3_chieu
            self.chay_3_chieu +=j.chay_3_chieu
            self.chao_3_chieu +=j.chao_3_chieu

            self.bun_chieu +=j.bun
            self.mi_chieu +=j.mi


        self.today_total_man_4 = self.man_trua + self.man_4_chieu
        self.today_total_chay_4 = self.chay_trua + self.chay_4_chieu
        self.today_total_chao_4 = self.chao_trua + self.chao_4_chieu

        self.today_total_man_3 = self.man_3_chieu
        self.today_total_chay_3 =self.chay_3_chieu
        self.today_total_chao_3 =self.chao_3_chieu

        self.today_total_bun = self.bun_chieu
        self.today_total_mi = self.mi_chieu

        self.money_man_4 = self.today_total_man_4 * self.price_man_4
        self.money_chay_4 = self.today_total_chay_4 * self.price_chay_4
        self.money_chao_4 = self.today_total_chao_4 * self.price_chao_4
        self.money_man_3 = self.today_total_man_3 * self.price_man_3
        self.money_chay_3 = self.today_total_chay_3 * self.price_chay_3
        self.money_chao_3 = self.today_total_chao_3 * self.price_chao_3
        self.money_bun = self.today_total_bun * self.price_bun
        self.money_dacbiet = self.price_dacbiet * self.dac_biet

        self.total_today = self.today_total_man_4 * self.price_man_4 + self.today_total_chay_4 * self.price_chay_4 +\
                           self.today_total_chao_4 * self.price_chao_4 + self.today_total_man_3 * self.price_man_3 +\
                           self.today_total_chay_3 * self.price_chay_3 + self.today_total_chao_3 * self.price_chao_3 +\
                           self.today_total_bun * self.price_bun + self.money_dacbiet


    def check_bophan_trua(self):
        list_bo_phan_trua = ['VPHONG','TMAY','CNC','CN1','CN2','MAU','VECNI','LRAP','CTRINH','TDO','KHO','QC','BTRI','IT']
        data_trua = self.env['bao.com'].search([('ngay_bao','=', self.ngay_bao),('com_buoi','=','trua')])
        for t in data_trua:
            list_bo_phan_trua.remove(t.bo_phan)
        if len(list_bo_phan_trua) > 0:
            raise exceptions.UserError(_('Những bộ phận chưa báo cơm trưa %s , Tổng %s') % (list_bo_phan_trua, len(list_bo_phan_trua)))
        else:
            raise UserError('Tất cả các bộ phận đã báo cơm trưa!')
    def check_bophan_chieu(self):
        list_bo_phan_chieu = ['VPHONG','TMAY','CNC','CN1','CN2','MAU','VECNI','LRAP','CTRINH','TDO','KHO','QC','BTRI','IT']
        data_chieu = self.env['bao.com'].search([('ngay_bao','=', self.ngay_bao),('com_buoi','=','chieu')])
        for c in data_chieu:
            list_bo_phan_chieu.remove(c.bo_phan)
        if len(list_bo_phan_chieu) > 0:
            raise exceptions.UserError(_('Những bộ phận chưa báo cơm chiều %s , Tổng %s') %(list_bo_phan_chieu, len(list_bo_phan_chieu)))
        else:
            raise UserWarning('Tất cả các bộ phận đã báo cơm chiều!')

    @api.multi
    def unlink(self):
        for i in self:
            if i.status == '1':
                raise UserError('bạn không thể xóa khi đã khóa!')
        return super(Nhansu, self).unlink()






        # print self._cr.dictfetchall()
        # print self._cr.fetchall()
        # print self._cr.self._cr.fetchone()

# self._cr.execute("your query")  # your query line
#
# from below two line you can use anyone based on your needs.
#
# result = self._cr.fetchall()  # return the data into list of tuple format
# result = self._cr.dictfetchall() # return the data into the list of dictionary format



