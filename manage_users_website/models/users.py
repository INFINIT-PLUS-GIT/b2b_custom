# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    belonging_company_id = fields.Many2one('res.partner', 'Belonging company', domain="[('is_company', '=', True)]")

    @api.model
    def toggle_user_active(self, uid):
        user = self.sudo().search([('id', '=', uid), '|', ('active', '=', False), ('active', '=', True)])
        user.sudo().write({
            'active': not user.active
        })
        self.env.cr.commit()

    @api.model
    def create_business_user(self, data):
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

    def get_portal_business_menu(self):
        query = """
            SELECT ma.portal_url, STRING_AGG(ma.id::character varying, ',') maids, MIN(ma.name) AS name, COUNT(ma.name) AS count
            FROM ir_model_access ma
            INNER JOIN res_groups rg ON ma.group_id = rg.id
            INNER JOIN res_groups_users_rel rgur on rg.id = rgur.gid
            WHERE ma.portal_url IS NOT NULL
              AND rg.category_id = (
                SELECT mc.id
                FROM ir_module_category mc
                WHERE mc.name = 'Business'
            )
            and rgur.uid = {}
            GROUP BY ma.portal_url
        """
        self._cr.execute(query.format(self.id))
        return self._cr.dictfetchall()
