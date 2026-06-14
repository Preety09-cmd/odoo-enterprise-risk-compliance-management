from odoo import models, fields


class RiskCategory(models.Model):
    _name = 'risk.management.category'
    _description = 'Risk Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
