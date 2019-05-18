# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import UserError
from datetime import date
import dateutil.parser

class Taisan(models.Model):
    _name = 'tai.san'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    img = fields.Binary(string='Hình ảnh', help="Hình ảnh tài sản, yêu cầu tỷ lệ kích thước: width(dài):height(cao) là 4:3 ")
    img_1 = fields.Binary(string='Hình ảnh 1')
    img_2 = fields.Binary(string='Hình ảnh 2')
    img_3 = fields.Binary(string='Hình ảnh 3')
    code = fields.Char(string='Mã thiết bị', default='New', readonly=True, help="Mã thiết bị là duy nhất, do LDS tự tạo và quy định cho mỗi thiết bị.")
    model_sp = fields.Char(string="Model sản phẩm",track_visibility='onchange', help='Model, mã sản phẩm...')
    name = fields.Char(string='Tên tài sản', track_visibility='onchange')
    gia_tri = fields.Integer(string='Giá trị', track_visibility='onchange', help="Giá trị thiết bị, Khuyến khích dùng đơn vị VNĐ")
    ngay_mua = fields.Date(string='Ngày mua' , track_visibility='onchange', help="Ngày mua thiết bị")
    bao_hanh_toi = fields.Date(string='Bảo hành tới', track_visibility='onchange', help='Ngày hết hạn bảo hành')
    nguoi_bao_quan = fields.Many2one('hr.employee',string='Người bảo quản', track_visibility='onchange', help="Người bảo quản thiết bị")
    status = fields.Selection([('0','Kho'),('1','Đang dùng'),('2','Phế')],string='Trạng thái',default='0',track_visibility='onchange',help="Trạng thái thiết bị")
    ngay_batdau_bao_quan = fields.Date(string="Từ khi", help="Là ngày Nhân viên bắt đầu nhận bảo quản")
    ly_do_phe = fields.Text(string='Lý do báo phế',track_visibility='onchange')
    ngay_bao_phe = fields.Date(string="Ngày báo phế",track_visibility='onchange', help="là ngày xếp ký đơn duyệt báo phế")
    nha_cung_cap = fields.Many2one('res.partner',string='Nhà cung cấp',domain=[('supplier','=',True)],track_visibility='onchange', help="Nhà cung cấp thiết bị")
    note = fields.Text(string='Ghi chú')
    kho = fields.Selection([('vp','Văn Phòng'),('sx','Sản Xuất')],string="Thuộc kho *", required=True,help="Thuộc Văn phòng hoặc Sản xuất, * là trường bắt buộc")
    het_bh = fields.Boolean(string='Hết bảo hành', default=False, compute='onchang_time')
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default= lambda self: self.env['res.company'].search([]).currency_id , help="Chú ý: Nên đổi ra giá trị của VNĐ để tiện việc thống kê Tổng giá trị TS", readonly=True)
    lich_su_bao_quan = fields.One2many('lich.su','ref_hr',string="Lịch sử bảo quản")
    so_luong = fields.Integer(string='Số lượng', default=1)
    ngay_con_bh = fields.Integer(string='Ngày còn bảo hành',compute='onchang_time')
    color = fields.Integer(default=0, compute='onchange_color')
    pdf_scan4 = fields.Binary(string="Giấy tờ liên quan 4", help='Các giấy tờ bảo hành liên quan!')
    pdf_scan1 = fields.Binary(string="Giấy tờ liên quan 1", help='Các giấy tờ bảo hành liên quan!')
    pdf_scan2 = fields.Binary(string="Giấy tờ liên quan 2", help='Các giấy tờ bảo hành liên quan!')
    pdf_scan3 = fields.Binary(string="Giấy tờ liên quan 3", help='Các giấy tờ bảo hành liên quan!')
    name_1 = fields.Char(string='Name1', default='dinh_kem_1')
    name_2 = fields.Char(string='Name2', default='dinh_kem_2')
    name_3 = fields.Char(string='Name3', default='dinh_kem_3')
    name_4 = fields.Char(string='Name4', default='dinh_kem_4')
    tinh_trang = fields.Selection([('new','Mới'),('old','Cũ'),('phe','Phế')], string='Tình trạng thiết bị')
    nguoi_moi = fields.Many2one('hr.employee', string='Người nhận thiết bị')
    luu_kho = fields.Boolean('Lưu kho phế', default= False, readonly=True)
    nguoi_nhan = fields.Many2one('res.users',string='Người nhận ts phế', readonly=True)
    da_ban = fields.Boolean(string='Đã bán', default=False,readonly=True)
    khach_hang =fields.Many2one('res.partner',string='Khách hàng', readonly=True)

    def _needaction_domain_get(self):
        return [('status', '=', '2'),('luu_kho','=',False)]


    @api.one
    @api.depends('het_bh','ngay_mua','bao_hanh_toi')
    def onchange_color(self):
        if self.ngay_mua and self.bao_hanh_toi:
            if self.het_bh == True:
                self.color = 2
            if self.het_bh == False:
                self.color = 5
        else:
            self.color = 0

    @api.one
    @api.depends('ngay_mua','bao_hanh_toi')
    def onchang_time(self):
        if self.ngay_mua and self.bao_hanh_toi:
            # year_m: nam mua, month_m: thang mua, day_m: ngay mua
            year_m = dateutil.parser.parse(self.ngay_mua).year
            month_m = dateutil.parser.parse(self.ngay_mua).month
            day_m =  dateutil.parser.parse(self.ngay_mua).day

            # year_bh, month_bh, day_bh: ngay thang nam het han bao hanh
            year_bh = dateutil.parser.parse(self.bao_hanh_toi).year
            month_bh = dateutil.parser.parse(self.bao_hanh_toi).month
            day_bh = dateutil.parser.parse(self.bao_hanh_toi).day

            d0 = date(year_m, month_m,day_m )
            d1 = date(year_bh, month_bh, day_bh)
            delta = abs(d0 - d1).days
            # delta la so ngay bao hanh tinh bang ngay (int)

            year_now = date.today().year
            month_now = date.today().month
            day_now = date.today().day
            d_now = date(year_now,month_now,day_now)
            time = abs(d_now - d0).days
            # time la thoi gian da su dung tinh bang ngay (int)
            if delta - time>0:
                self.ngay_con_bh = delta - time
            else:
                self.ngay_con_bh = 0
                self.het_bh = True
    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('code_code') or '/'
        return super(Taisan, self).create(vals)

    @api.multi
    def confirm(self):
        if self.nguoi_bao_quan and self.ngay_batdau_bao_quan:
            self.write({'status': '1'})
            hist = self.search([('code', '=', self.code)])
            hist.write({
            'lich_su_bao_quan': [(0, 0, {
                'his_type': 'bq',
                'note': '',
                'nguoi_bq': self.nguoi_bao_quan.name,
                'so_the': self.nguoi_bao_quan.so_the,
                'thiet_bi': self.code,
                'tu_ngay': self.ngay_batdau_bao_quan
        })]

            })
        elif self.nguoi_bao_quan is not True or self.ngay_batdau_bao_quan is not True:
            self.write({'status': '0'})
            raise UserError (_('Cần có người bảo quản, Ngày bắt đầu bảo quản'))
        self.env['top.10'].get_data()

    @api.multi
    def _create_his(self):
        print 'aaaa'
        # tạo lịch sử bảo quản tài sản bên nhân viên
        hist_bq = self.env['hr.employee'].search([('so_the', '=', self.nguoi_bao_quan.so_the)])
        hist_bq.write({
            'lich_su': [(0, 0, {
                'tu_ngay': self.ngay_batdau_bao_quan,
                'note': '',
                'toi_ngay': date.today(),
                'ten_thiet_bi': self.name,
                'ma_thiet_bi': self.code
            })]
        })

    # trả kho
    @api.multi
    def unconfirm(self):
        hist = self.search([('code', '=', self.code)])
        hist.write({
            'lich_su_bao_quan': [(0, 0, {
                'his_type': 'kho',
                'note': '',
                'tu_ngay': date.today(),
                'thiet_bi': self.code,
                'nguoi_bq': self.nguoi_bao_quan.name,
                'so_the': self.nguoi_bao_quan.so_the,
            })]

        })

        self._create_his()
        self.env['hr.employee'].search([('thiet_bi.code', '=', self.code)]).write({'thiet_bi': [(3, self.id)]})
        self.nguoi_bao_quan = False
        self.write({'status':'0'})
        self.env['top.10'].get_data()
        self.luu_kho = False
        self.tinh_trang= 'old'
        self.nguoi_nhan = False

    # báo phế
    @api.multi
    def cancel(self):
        if not self.ly_do_phe or not self.ngay_bao_phe:
            raise UserError('Cần có lý do và ngày báo phế!')

        hist = self.search([('code', '=', self.code)])
        hist.write({
            'lich_su_bao_quan': [(0, 0, {
                'his_type': 'phe',
                'note': '',
                'tu_ngay': self.ngay_bao_phe,
                'thiet_bi': self.code,
                'nguoi_bq': self.nguoi_bao_quan.name,
                'so_the': self.nguoi_bao_quan.so_the,
            })]
        })

        self._create_his()
        self.env['hr.employee'].search([('thiet_bi.code', '=', self.code)]).write({'thiet_bi': [(3, self.id)]})
        self.nguoi_bao_quan = False
        self.write({'status':'2'})
        self.env['top.10'].get_data()
        self.tinh_trang = 'phe'
        self.luu_kho = False

    def luukho(self):
        self.luu_kho = True
        self.nguoi_nhan = self.env.user
        hist = self.search([('code', '=', self.code)])
        hist.write({
            'lich_su_bao_quan': [(0, 0, {
                'his_type': 'nhap_kho_phe',
                'note': '',
                'tu_ngay': date.today(),
                'thiet_bi': self.code,
                'nguoi_bq': self.nguoi_nhan.name,

            })]
        })

    def confirm_chuyen(self):
        if self.nguoi_moi:
            hist = self.search([('code', '=', self.code)])
            hist.write({
                'lich_su_bao_quan': [(0, 0, {
                    'his_type': 'dich_chuyen',
                    'note': '',
                    'tu_ngay': date.today(),
                    'thiet_bi': self.code,
                    'nguoi_bq': self.nguoi_bao_quan.name,
                    'so_the': self.nguoi_bao_quan.so_the,
                    'nguoi_moi': self.nguoi_moi.name,
                    'so_the_moi': self.nguoi_moi.so_the,

                })]

            })
            self.ngay_batdau_bao_quan = date.today()
            self.tinh_trang = 'old'
            self._create_his()
            self.env['hr.employee'].search([('thiet_bi.code', '=', self.code)]).write({'thiet_bi': [(3, self.id)]})
            # self.nguoi_bao_quan = False
            self.nguoi_bao_quan = self.nguoi_moi
            self.nguoi_moi = False
            self.env['top.10'].get_data()
        else: raise UserError('Cần có người mới nhận BQ thiết bị!')

    @api.multi
    def unlink(self):
        if self.status in ('1','2'):
            raise UserError('Không được xóa thiết bị khỏi hệ thống!')
        else:
            return super(Taisan, self).unlink()