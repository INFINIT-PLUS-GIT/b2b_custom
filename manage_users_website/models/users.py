# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    belonging_company_id = fields.Many2one('res.partner', 'Belonging company', domain="[('is_company', '=', True)]")

    @api.model
    def create_user(self, data):
        print('inside python function')
        print(data)
        logged_user = self.env.user
        self.sudo().create({
            'name': data['user-name'],
            'login': data['user-email'],
            # 'name': data['user-role'],
            'password': data['user-password']
        })
        return {
            "status": "ok"
        }
