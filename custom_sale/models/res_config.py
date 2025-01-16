from odoo import api, fields, models, _, exceptions



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_order_limit = fields.Float(
        string="Sale Order Limit")
