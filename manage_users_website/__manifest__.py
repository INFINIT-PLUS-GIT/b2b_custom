# -*- coding: utf-8 -*-
{
    'name': "<anage users website",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Infinit Plus",
    'website': "https://www.infinit-plus.com",

    'category': 'Uncategorized',
    'version': '14.0.1',

    'depends': [
        'base',
        'website'
    ],

    'data': [
        'security/ir.model.access.csv',
        'security/res_group.xml',
        'views/assets.xml',
        'views/user_create.xml',
        'views/business_users.xml',
        'views/portal_users.xml',
        'views/groups_view.xml',
    ],
}
