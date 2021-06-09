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
        read = False
        create = False
        write = False
        maids = data.get('maids')
        if maids:
            accesses = self.env['ir.model.access'].sudo().search([('id', 'in', maids.split(','))])
            for access in accesses:
                read = access.perm_read or read
                create = access.perm_create or create
                write = access.perm_write or write

        role_id = data['role']
        del data['role']
        del data['maids']
        if data.get('uid'):
            if not write:
                return {
                    "status": "not-allowed"
                }
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
            if not create:
                return {
                    "status": "not-allowed"
                }
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
            and ma.perm_read is true
            GROUP BY ma.portal_url
        """
        self._cr.execute(query.format(self.id))
        return self._cr.dictfetchall()
