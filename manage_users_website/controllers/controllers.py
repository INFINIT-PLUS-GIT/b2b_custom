# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ManageUsersWebsite(http.Controller):

    @http.route(['/my/business/users/manager', '/my/business/users/manager/<int:uid>'], type="http", auth='user', website=True)
    def object(self, uid=None, **kw):
        user = request.env['res.users'].sudo().browse(uid)
        url_params = dict(kw)
        read = False
        create = False
        write = False
        maids = url_params.get('maids')
        if maids:
            accesses = request.env['ir.model.access'].sudo().search([('id', 'in', maids).split(',')])
            for access in accesses:
                read = access.perm_read or read
                create = access.perm_create or create
                write = access.perm_write or write
        data = {
            'access_rights': {
                'read': read,
                'create': create,
                'write': write
            },
            'maids': maids
        }
        role_id = None
        group_categ = request.env['ir.module.category'].sudo().search([('name', '=', 'Business')])
        for group in request.env['res.groups'].sudo().search([('category_id', '=', group_categ.id)]):
            if group.id in user.groups_id.ids:
                role_id = group.id
        if user:
            data.update({
                'uid': uid,
                'name': user.name,
                'login': user.login,
                'role': role_id,
                'password': 'password'
            })
        return request.render('manage_users_website.management_user_form', {'data': data})
