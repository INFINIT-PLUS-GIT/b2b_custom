# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    belonging_company_id = fields.Many2one('res.partner', 'Belonging company', domain="[('is_company', '=', True)]")

    @api.model
    def deactivate_user(self, uid):
        user = self.sudo().search([('id', '=', uid)])
        user.write({
            'active': False
        })

    @api.model
    def create_user(self, data):
        role_id = data['role']
        del data['role']
        if data.get('uid'):
            user = self.sudo().search([('id', '=', data.get('uid'))])
            user.sudo().write({
                'groups_id': [[6, 0, []]]
            })
            user.sudo().write({
                'name': data['name'],
                'login': data['login'],
                'belonging_company_id': self.env.user.belonging_company_id.id,
                'groups_id': [[6, 0, [role_id, self.env.ref('base.group_portal').id]]]
            })
        else:
            del data['uid']
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
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    belonging_company_id = fields.Many2one('res.partner', 'Belonging company', domain="[('is_company', '=', True)]")

    @api.model
    def deactivate_user(self, uid):
        user = self.sudo().search([('id', '=', uid)])
        user.write({
            'active': False
        })

    @api.model
    def create_user(self, data):
        role_id = data['role']
        del data['role']
        if data.get('uid'):
            user = self.sudo().search([('id', '=', data.get('uid'))])
            user.sudo().write({
                'groups_id': [(5, 0, [])]
            })
            user.sudo().write({
                'name': data['name'],
                'login': data['login'],
                'belonging_company_id': self.env.user.belonging_company_id.id,
                'groups_id': [(6, 0, [role_id, self.env.ref('base.group_portal').id])]
            })
        else:
            del data['uid']
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
