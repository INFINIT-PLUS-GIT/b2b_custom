# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    belonging_company_id = fields.Many2one('res.partner', 'Belonging company', related='partner_id.user_ids.belonging_company_id')
