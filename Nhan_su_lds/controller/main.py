# -*- coding: utf-8 -*-
from odoo import http
import datetime, time
from odoo import models, fields, api

class ThongBao(http.Controller):
    @http.route('/page/img', auth='public', website=True)
    def index(self, **kw):
        ThongBao = http.request.env['nhan.su']
        return http.request.render('Nhan_su_lds.img',
                                   {'sv': ThongBao.sudo().search([('ngay_bao', '=', datetime.date.today())])
                                    })
class Author(http.CommonController):
    @http.route('/page/author', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('Nhan_su_lds.lvquy')


class Index(http.Controller):
    @http.route('/page/baocom', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('Nhan_su_lds.default_get_data')

    @http.route(['/Nhan_su_lds/insert_data_info'], type='http', methods=['POST'], auth='public', website=True,
                csrf=False)
    def func_submit(self, **post):
        if post['com_buoi'] == 'trua':
            post['man_4_chieu']=post['chay_4_chieu']=post['chao_4_chieu']=post['man_3_chieu']=post['chay_3_chieu']=post['chao_3_chieu']=post['bun']=post['mi']=0
        if post['com_buoi'] == 'chieu':
            post['man_trua'] = post['chay_trua'] = post['chao_trua'] = 0

        data = http.request.env['bao.com']
        setting = http.request.env['setting'].search([])
        vals = {
            'com_buoi': post['com_buoi'],
            'com_chay_trua': post['chay_trua'],
            'com_man_trua': post['man_trua'],
            'chao_trua': post['chao_trua'],

            'man_4_chieu': post['man_4'],
            'chay_4_chieu': post['chay_4'],
            'chao_4_chieu': post['chao_4'],
            'man_3_chieu': post['man_3'],
            'chay_3_chieu': post['chay_3'],
            'chao_3_chieu': post['chao_3'],
            'bun': post['bun'],
            'mi': post['mi'],
            'note': post['note'],
        }


        # kiểm tra lỗi, chỉ cho báo cơm trong 1 khoảng thời gian,


        hour = datetime.datetime.today().hour + 7
        mins = datetime.datetime.today().minute

        time_s_1 = datetime.time(hour=setting.sang1_h, minute=setting.sang1_m)
        time_s_2 = datetime.time(hour=setting.sang2_h, minute=setting.sang2_m)

        time_c_2 = datetime.time(hour=setting.chieu2_h, minute=setting.chieu2_m)
        now = datetime.time(hour=hour, minute=mins)


        if (now < time_s_1)  or (now > time_c_2):
            return http.request.render('Nhan_su_lds.loi_time')
        if (now >= time_s_2) and (post['com_buoi'] == 'trua'):
            return http.request.render('Nhan_su_lds.loi_time_trua')

        # kiểm tra chỉ được báo cơm 1 lần
        # Văn phòng
        if http.request.env.user.bo_phan == 'VPHONG':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','VPHONG'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','VPHONG'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')

        # Tổ máy
        if http.request.env.user.bo_phan == 'TMAY':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','TMAY'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','TMAY'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # CNC
        if http.request.env.user.bo_phan == 'CNC':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CNC'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CNC'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # Chà nhám 1
        if http.request.env.user.bo_phan == 'CN1':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CN1'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CN1'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # Chà nhám 2
        if http.request.env.user.bo_phan == 'CN2':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CN2'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CN2'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # Tổ mẫu
        if http.request.env.user.bo_phan == 'MAU':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','MAU'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','MAU'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # VECNI
        if http.request.env.user.bo_phan == 'VECNI':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','VECNI'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','VECNI'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')

        # lắp ráp
        if http.request.env.user.bo_phan == 'LRAP':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','LRAP'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','LRAP'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # Công trình
        if http.request.env.user.bo_phan == 'CTRINH':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CTRINH'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','CTRINH'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # Tiến độ
        if http.request.env.user.bo_phan == 'TDO':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','TDO'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','TDO'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # Kho
        if http.request.env.user.bo_phan == 'KHO':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','KHO'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','KHO'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # QC
        if http.request.env.user.bo_phan == 'QC':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','QC'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','QC'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')
        # Bảo trì
        if http.request.env.user.bo_phan == 'BTRI':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','BTRI'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','BTRI'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')

        # IT
        if http.request.env.user.bo_phan == 'IT':
            if post['com_buoi'] == 'trua':
                if http.request.env['bao.com'].search_count([('bo_phan','=','IT'),('com_buoi','=','trua'),('ngay_bao','=', datetime.date.today())]) >0:
                    return http.request.render('Nhan_su_lds.loi')
            if post['com_buoi'] == 'chieu':
                if http.request.env['bao.com'].search_count([('bo_phan','=','IT'),('com_buoi','=','chieu'),('ngay_bao', '=', datetime.date.today())]) > 0:
                    return http.request.render('Nhan_su_lds.loi_c')

        data.create(vals)
        return http.request.render('Nhan_su_lds.thank')
