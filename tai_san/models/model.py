# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError

class HR(models.Model):
    _inherit = 'hr.employee'
    _order = 'tong_gt_ts desc'

    email_noibo = fields.Char(string="Email nội bộ")
    work_email = fields.Char(string="Email ngoại bộ")
    so_the = fields.Char(string="Số thẻ", help='Số thẻ nhân viên', required=True)
    _sql_constraints = [
        ('so_the_uniq', 'UNIQUE(so_the)', 'Số thẻ này đã tồn tại, Kiểm tra lại!')
    ]
    thiet_bi = fields.One2many('tai.san','nguoi_bao_quan',string='Thiet bi')
    server = fields.Char(string="Server lưu trữ")
    count_ts = fields.Integer(string='Tổng tài sản bảo quản', compute='ts_count', )
    tong_gt_ts = fields.Integer(string='Tổng giá trị bảo quản', compute='ts_count', store=True)
    lich_su = fields.One2many('lich.subq','ref_a', string='Lịch sử bảo quản')

    @api.one
    @api.depends('thiet_bi')
    def ts_count(self):
        self.count_ts  =  len(self.thiet_bi)
        for i in self.thiet_bi:
            self.tong_gt_ts += i.gia_tri

    @api.multi
    def unlink(self):
        if self.thiet_bi:
            raise UserError('Không xóa được khi còn thiết bị bảo quản')
        else:
            return super(HR, self).unlink()

class Lichsu(models.Model):
    _name='lich.su'

    ref_hr = fields.Many2one('tai.san')
    thiet_bi = fields.Char(string="Thiết bị")
    nguoi_bq = fields.Char(string="Người bảo quản")
    so_the = fields.Char(string='Số thẻ')
    nguoi_moi = fields.Char(string="Người mới")
    so_the_moi = fields.Char(string='Số thẻ người mới')
    note = fields.Text(string='Note')
    tu_ngay = fields.Date(string='Từ ngày')
    his_type = fields.Selection([('bq','Bắt đầu bảo quản'),
                                 ('kho','Trả kho'),
                                 ('phe','Đã báo phế'),
                                 ('dich_chuyen','Dịch chuyển BQ'),
                                 ('nhap_kho_phe','Nhập kho phế'),
                                 ('ban_phe_lieu','Bán phế liệu'),
                                 ],string='Thuộc Kiểu')


class LichSuBQ(models.Model):
    _name = 'lich.subq'

    ref_a = fields.Many2one('hr.employee')
    tu_ngay = fields.Date(string='Từ ngày')
    toi_ngay = fields.Date(string='Tới ngày')
    ma_thiet_bi = fields.Char(string='Mã thiết bị bảo quản')
    ten_thiet_bi = fields.Char(string='Tên thiết bị bảo quản')
    note= fields.Text(string='Ghi chú')

class Top10(models.Model):
    _name = 'top.10'
    _order = 'tong_gt_bq desc'

    tong_gt_bq = fields.Integer(string='Tổng giá trị bảo quản',store=True, related='name.tong_gt_ts')
    name = fields.Many2one('hr.employee', string='Tên nhân viên')
    so_the= fields.Char(related='name.so_the', string='Số thẻ')
    so_luong= fields.Integer(related='name.count_ts', string='Tổng số tài sản BQ')
    bo_phan = fields.Char(related='name.department_id.name', string='Bộ phận')
    no = fields.Integer(string='NO')

    def get_data(self):
        # print "Geting....."
        data = self.env['hr.employee'].search([],limit=10, order='tong_gt_ts desc')

        self.search([]).unlink()
        k=1
        for i in data:
            self.create({'name':i.id, 'no':k})
            k+=1