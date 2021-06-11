# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request


class PortalUsers(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalUsers, self)._prepare_portal_layout_values()
        business_users_count = request.env['res.users'].search_count([
            ('belonging_company_id', '=', request.env.user.belonging_company_id.id), '|',
            ('active', '=', False), ('active', '=', True)])
        values['business_users_count'] = business_users_count
        return values

    @http.route(['/my/business/payments', '/my/business/payments/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_transactions(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        url_params = dict(kw)
        read = False
        create = False
        write = False
        maids = url_params.get('maids')
        if maids:
            accesses = request.env['ir.model.access'].sudo().search([('id', 'in', maids.split(','))])
            for access in accesses:
                read = access.perm_read or read
                create = access.perm_create or create
                write = access.perm_write or write
        else:
            return request.redirect('/my/home')
        if not read:
            return request.redirect('/my/home')
        values = self._prepare_portal_layout_values()
        business_payments = request.env['account.move']

        domain = [('move_type', 'in', ['out_invoice', 'out_refund'])]

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive_groups = self._get_archive_groups('payment.transaction')
        if date_begin and date_end:
            domain += [('data', '>', date_begin), ('date', '<=', date_end)]

        # count for pager
        business_payments_count = business_payments.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/business/payments",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=business_payments_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        invoices = business_payments.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        # request.session['my_transactions_history'] = transactions.ids[:100]

        values.update({
            'date': date_begin,
            'invoices': invoices,
            'page_name': 'business_payments',
            'pager': pager,
            'default_url': '/my/business/payments',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'access_rights': {
                'read': read,
                'create': create,
                'write': write
            },
            'maids': maids
        })
        return request.render("manage_payments_website.portal_my_business_invoices", values)
