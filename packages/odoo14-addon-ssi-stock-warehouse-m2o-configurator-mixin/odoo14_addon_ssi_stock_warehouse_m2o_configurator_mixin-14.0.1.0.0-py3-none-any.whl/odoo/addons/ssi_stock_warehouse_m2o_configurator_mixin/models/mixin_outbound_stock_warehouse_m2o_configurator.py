# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinOutboundStockWarehouseM2OConfiguratorck(models.AbstractModel):
    _name = "mixin.outbound_stock_warehouse_m2o_configurator"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "stock.warehouse Many2one Configurator Mixin"

    _outbound_stock_warehouse_m2o_configurator_insert_form_element_ok = False
    _outbound_stock_warehouse_m2o_configurator_form_xpath = False

    outbound_warehouse_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Outbound Warehouse Selection Method",
        required=True,
    )
    outbound_warehouse_ids = fields.Many2many(
        comodel_name="stock.warehouse",
        string="Outbound Warehouses",
        relation="rel_m2o_configurator_2_outbound_stock_warehouse",
    )
    outbound_warehouse_domain = fields.Text(
        default="[]", string="Outbound Warehouse Domain"
    )
    outbound_warehouse_python_code = fields.Text(
        default="result = []", string="Outbound Warehouse Python Code"
    )

    @ssi_decorator.insert_on_form_view()
    def _outbound_stock_warehouse_m2o_configurator_insert_form_element(self, view_arch):
        # TODO
        template_xml = "ssi_stock_warehouse_m2o_configurator_mixin."
        template_xml += "outbound_stock_warehouse_m2o_configurator_template"
        if self._outbound_stock_warehouse_m2o_configurator_insert_form_element_ok:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id=template_xml,
                xpath=self._outbound_stock_warehouse_m2o_configurator_form_xpath,
                position="inside",
            )
        return view_arch
