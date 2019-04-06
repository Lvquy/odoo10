# -*- coding:utf-8 -*-
from odoo import models, fields, api
import pushbullet
import dateutil.parser


class APIKEY(models.Model):
    _name = 'api.key'

    api_key = fields.Char(string='API KEY', required=True)
    name = fields.Char(string='Name')
    mobile = fields.Char(string="Mobile", required=True)
    email = fields.Char(string="Email", required=True)
    create_date =fields.Datetime(string="Date create")
    hide = fields.Boolean(string="Hide token", default=False)
    status = fields.Selection([('off','OFF'),('on','ON')],default='off',string='Trạng thái API')

    def test(self):
        pb = pushbullet.Pushbullet(self.api_key)
        device = pb.devices[0]
        # pb.push_sms(device,self.mobile,'API SMS: Thành công rồi, haha')
    def change_status(self):
        if self.status == 'off':
            self.test()
            stt_on = self.env['api.key'].search([('status','=','on')],limit=1)
            if stt_on.status:
                print stt_on.status
                stt_on.status = 'off'
            self.status = 'on'
        elif self.status =='on':
            self.status = 'off'

class Push_Vendor(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_confirm(self):
        if self.env['api.key'].search([],limit=1).status == 'on':
            for order in self:
                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order.company_id.po_double_validation == 'one_step' \
                        or (order.company_id.po_double_validation == 'two_step' \
                            and order.amount_total < self.env.user.company_id.currency_id.compute(
                            order.company_id.po_double_validation_amount, order.currency_id)) \
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
                # --------- Push SMS Notification --------
            po = str(self.name)
            amount_total = str(self.amount_total)
            vendor = str(self.partner_id.name).title()
            mobile = str(self.partner_id.mobile)
            currency_id = str(self.currency_id.name)
            date_order = str(dateutil.parser.parse(self.date_order).date())
            sms = 'Chào bạn ' + vendor + ', đơn hàng ' + po + ' đã xác nhận.' + ' Giá trị đơn hàng: ' + amount_total + ' ' + currency_id + '. Ngày đặt hàng: ' + date_order

            # pb.push_sms(device, mobile, sms)
            pb = pushbullet.Pushbullet(self.env['api.key'].search([],limit=1).api_key)
            device = pb.devices[0]
            pb.push_sms(device,mobile,sms)
            return True
        else:
            for order in self:
                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order.company_id.po_double_validation == 'one_step' \
                        or (order.company_id.po_double_validation == 'two_step' \
                            and order.amount_total < self.env.user.company_id.currency_id.compute(
                            order.company_id.po_double_validation_amount, order.currency_id)) \
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
            return True

