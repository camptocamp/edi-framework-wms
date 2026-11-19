# Copyright 2026 Camptocamp SA
# @author Hadrien Huvelle <hadrien.huvelle@camptocamp.com>
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockExternalInventoryReport(models.Model):
    _name = "stock.external.inventory.report"
    _inherit = ["stock.external.inventory.report", "edi.exchange.consumer.mixin"]

    backend_id = fields.Many2one(
        "edi.backend",
        readonly=True,
        index=True,
        ondelete="restrict",
        help="WMS backend that sent the report.",
    )
