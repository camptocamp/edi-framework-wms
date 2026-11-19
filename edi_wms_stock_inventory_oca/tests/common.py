# Copyright 2026 Camptocamp SA
# @author Hadrien Huvelle <hadrien.huvelle@camptocamp.com>
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo.addons.stock_external_inventory_report.tests.common import (
    InventoryReportCommon as BaseInventoryReportCommon,
)


class InventoryReportCommon(BaseInventoryReportCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, edi__skip_quick_exec=True))
        cls._setup_backend()

    @classmethod
    def _setup_backend(cls):
        """Set up the WMS backend and the inventory report exchange type."""
        backend_type = cls.env["edi.backend.type"].create(
            {"name": "Test WMS", "code": "test_edi_wms_stock_inventory", "wms": True}
        )
        cls.backend = cls.env["edi.backend"].create(
            {
                "name": "Test WMS",
                "backend_type_id": backend_type.id,
                "warehouse_id": cls.warehouse.id,
            }
        )
        cls.exchange_type = cls.env["edi.exchange.type"].create(
            {
                "name": "Test WMS inventory report",
                "code": "test_edi_wms_stock_inventory_report",
                "backend_type_id": backend_type.id,
                "backend_id": cls.backend.id,
                "direction": "input",
                "exchange_file_ext": "json",
                "process_model_id": cls.env["ir.model"]._get_id(
                    "edi.wms.inventory.report.handler.process"
                ),
            }
        )

    @classmethod
    def _create_incoming_exchange(cls, payload):
        exchange = cls.backend.with_context(edi__skip_quick_exec=True).create_record(
            cls.exchange_type.code,
            {"edi_exchange_state": "input_received"},
        )
        exchange._set_file_content(json.dumps(payload))
        return exchange
