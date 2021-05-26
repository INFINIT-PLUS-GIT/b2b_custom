# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    belonging_company_id = fields.Many2one('res.partner', 'Belonging company', domain="[('is_company', '=', True)]")

    @api.model
    def create_user(self, data):
        print('inside python function')
        print(data)
        role_id = data['role']
        del data['role']
        logged_user = self.env.user
        db, login, password = self.sudo().signup(data, '')
        user = self.sudo().search([('login', '=', login)])
        user.sudo().write({
            'belonging_company_id': self.env.user.belonging_company_id.id,
            'groups_id': [[6, 0, [role_id, self.env.ref('base.group_portal').id]]]
        })
        self.env.cr.commit()
        return {
            "status": "ok"
        }
