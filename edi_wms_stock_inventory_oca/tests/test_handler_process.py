# Copyright 2026 Camptocamp SA
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from .common import InventoryReportCommon


class TestHandlerProcess(InventoryReportCommon):
    """The handler turns an exchange record into a report and compares it."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.handler = cls.env["edi.wms.inventory.report.handler.process"]

    def _process(self, exchange, report_vals, lines_vals):
        """Process ``exchange`` with a parser returning the given values."""
        handler_cls = type(self.handler)
        with (
            patch.object(
                handler_cls, "_parse_payload", return_value=(report_vals, lines_vals)
            ) as parse,
            patch.object(
                type(self.env["stock.external.inventory.report"]),
                "process_comparisons_and_alerts",
                autospec=True,
            ) as compare,
        ):
            self.handler.process(exchange)
        return parse, compare

    def test_process(self):
        """The report of the backend's warehouse is linked to its exchange."""
        exchange = self._create_incoming_exchange({"report_date": "REH"})
        parse, compare = self._process(
            exchange,
            {"report_date": "2026-02-01 00:00:00"},
            [{"external_product_code": "INV-001", "external_qty": 4.0}],
        )
        parse.assert_called_once_with(exchange, {"report_date": "REH"})
        exchange.invalidate_recordset(["model", "res_id"])
        report = exchange.record
        self.assertEqual(report._name, "stock.external.inventory.report")
        self.assertEqual(report.external_reference, exchange.identifier)
        self.assertEqual(report.backend_id, self.backend)
        self.assertEqual(report.warehouse_id, self.warehouse)
        self.assertEqual(report.line_ids.external_product_code, "INV-001")
        compare.assert_called_once_with(report)

    def test_process_keeps_reference(self):
        """The reference given by the payload is kept."""
        exchange = self._create_incoming_exchange({})
        self._process(exchange, {"external_reference": "REF-1"}, [])
        exchange.invalidate_recordset(["model", "res_id"])
        self.assertEqual(exchange.record.external_reference, "REF-1")

    def test_parse_payload_not_implemented(self):
        """The payload format is left to the handler of each WMS."""
        exchange = self._create_incoming_exchange({})
        with self.assertRaises(NotImplementedError):
            self.handler.process(exchange)
