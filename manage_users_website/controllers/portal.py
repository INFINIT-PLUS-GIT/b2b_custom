# -*- coding: utf-8 -*-

from odoo import http, _
import requests
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request


class PortalAccount(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalAccount, self)._prepare_portal_layout_values()
        business_users_count = request.env['res.users'].search_count([('belonging_company_id', '=', request.env.user.belonging_company_id.id)])
        values['business_users_count'] = business_users_count
        return values

    @http.route(['/my/business/users', '/my/business/users/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_transactions(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        business_users = request.env['res.users']

        domain = [('belonging_company_id', '=', request.env.user.belonging_company_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        #archive_groups = self._get_archive_groups('payment.transaction')
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        business_users_count = business_users.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/business/users",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=business_users_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        users = business_users.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        # request.session['my_transactions_history'] = transactions.ids[:100]

        values.update({
            'date': date_begin,
            'users': users,
            'page_name': 'business_users',
            'pager': pager,
            'default_url': '/my/business/users',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("manage_users_website.portal_my_business_users", values)
