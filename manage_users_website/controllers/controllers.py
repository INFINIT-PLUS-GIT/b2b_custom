# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ManageUsersWebsite(http.Controller):

    @http.route('/user_manager/create_user', type="http", auth='user', website=True)
    def object(self, **kw):
        return request.render('manage_users_website.management_user_form', {})
