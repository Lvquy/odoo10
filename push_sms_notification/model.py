# -*- coding:utf-8 -*-
from pushbullet import Pushbullet
from odoo import api, fields, models
import dateutil.parser


API_KEY ='o.08l11dgmJ0Et9LZRJei5EPUJ6onmAmfL'
pb = Pushbullet(API_KEY)
device = pb.devices[0]

class Push_Vendor(models.Model):
    _inherit = 'purchase.order'
    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id)) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            # --------- Push SMS Notification --------
            note = ''
            po = str(self.name)
            amount_total = str(self.amount_total)
            vendor = str(self.partner_id.name).title()
            mobile = str(self.partner_id.mobile)
            currency_id = str(self.currency_id.name)
            date_order =  str(dateutil.parser.parse(self.date_order).date())

            note = 'Chào bạn ' + vendor + ', đơn hàng ' + po + ' đã xác nhận.' + ' Giá trị đơn hàng: ' + amount_total + ' ' + currency_id + '. Ngày đặt hàng: '+ date_order
            pb.push_note("Thông báo từ odoo", note)
            pb.push_sms(device, mobile, note)
        return True

class Push_Customer(models.Model):
    _inherit = 'sale.order'
    @api.multi
    def action_confirm(self):
        for order in self:
            order.state = 'sale'
            order.confirmation_date = fields.Datetime.now()
            if self.env.context.get('send_email'):
                self.force_quotation_send()
            order.order_line._action_procurement_create()
        if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
            self.action_done()

        # --------- Push SMS Notification --------
        so = str(self.name)
        amount_total = str(self.amount_total)
        customer = str(self.partner_id.name).title()
        mobile = str(self.partner_id.mobile)
        currency_id = str(self.currency_id.name)
        confirm_date = str(dateutil.parser.parse(self.confirmation_date).date())
        note = 'Chào bạn '+ customer + ', đơn hàng ' + so  + ' đã xác nhận.' + ' Giá trị đơn hàng: ' + amount_total + ' '+currency_id + '. Ngày xác nhận: '+ confirm_date
        pb.push_note("Thông báo từ odoo", note)
        pb.push_sms(device, mobile, note)
        return True
class Test_cron(models.Model):
    _name = 'test.cron'
    _inherit = 'hr.employee'

    @api.model
    def auto_notifi(self):
        for i in self.env['hr.employee'].search([('department_id.name','=','Administration')]):
            pb.push_note("Xin chào bạn: ", i.name)
        print 'helooooooooooooooooooooooooooooo'