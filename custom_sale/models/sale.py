from odoo import api, fields, models, _, exceptions



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_reference = fields.Char(string="Manager Reference", help="Reference provided by the manager")
    auto_workflow = fields.Boolean(string="Auto Workflow",
                                   help="Automate the entire workflow upon confirming the Sale Order")

    def action_confirm(self):
        config_settings = self.env['res.config.settings'].search([], limit=1)
        sale_order_limit = config_settings.sale_order_limit if config_settings else 0.0
        if self.amount_total > float(sale_order_limit):
            if not self.env.user.has_group('custom_sale.group_sale_admin'):
                raise exceptions.UserError(
                    "You are not allowed to confirm this sale order as the amount exceeds the defined limit and you do not have the required permission."
                )

        res = super(SaleOrder, self).action_confirm()

        if self.auto_workflow:
            for order in self:
                pickings = order.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel'])
                for picking in pickings:
                    picking.action_confirm()
                    picking.action_assign()
                    picking.button_validate()


                invoice = order._create_invoices()
                invoice.action_post()


        return res

    def _create_delivery(self, line):
        """Create a delivery for a specific line."""
        picking_vals = {
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'location_id': self.warehouse_id.lot_stock_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id,
            'move_ids_without_package': [(0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'name': line.name,
                'location_id': self.warehouse_id.lot_stock_id.id,
                'location_dest_id': self.partner_id.property_stock_customer.id,
            })]
        }
        return self.env['stock.picking'].create(picking_vals)



