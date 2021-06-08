from odoo import models, fields


class IrModelAccess(models.Model):
    _inherit = 'ir.model.access'

    portal_url = fields.Char('Portal page url')
