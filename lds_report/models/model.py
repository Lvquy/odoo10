# -*- coding: utf-8 -*-
# ITCV 2018-01-20 11:08
# =============================================================================#
# TinyERP, Open Source Management Solution                                    #
# Tel:01699327988  E-mail:sales@3c4g.net  zhaohuaw@gmail.com                  #
# Copyright (C) 2013-2017  CTY TNHH MTV BA C BON G  (http://www.tinyERP.net)  #
# =============================================================================#
from odoo import api, fields, models, tools, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    LDS_ETD = fields.Date(string="LDS ETD", index=True)
    LDS_ETA = fields.Date(string="LDS ETA", index=True)
    LDS_NO = fields.Char(string="LDS NO")

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['LDS_ETD'] = self.LDS_ETD
        invoice_vals['LDS_ETA'] = self.LDS_ETA
        invoice_vals['LDS_NO'] = self.LDS_NO
        return invoice_vals


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    LDS_ETD = fields.Date(string="LDS ETD")
    LDS_ETA = fields.Date(string="LDS ETA")
    LDS_PINO = fields.Char(sting="LDS PI NO")
    LDS_PONO = fields.Char(sting="LDS PO NO")
    LDS_NO = fields.Char(sting="LDS NO")
    LDS_Words_Total = fields.Char(sting="amount in words")


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    LDS_IMG1 = fields.Binary(string="LDS IMG1")
    LDS_IMG2 = fields.Binary(string="LDS IMG2")
    LDS_IMG3 = fields.Binary(string="LDS IMG3")
    LDS_IMG4 = fields.Binary(string="LDS IMG4")
    LDS_IMG5 = fields.Binary(string="LDS IMG5")
    LDS_IMG6 = fields.Binary(string="LDS IMG6")


    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
