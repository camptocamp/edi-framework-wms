# Copyright 2026 Camptocamp SA
# @author Hadrien Huvelle <hadrien.huvelle@camptocamp.com>
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo import models
from odoo.fields import Command


class EdiWmsInventoryReportHandlerProcess(models.AbstractModel):
    _name = "edi.wms.inventory.report.handler.process"
    _inherit = "edi.oca.handler.process"
    _description = "Process a WMS inventory report"

    def process(self, exchange_record):
        """Create the inventory report of the exchange record.

        The report is created in the processing of the exchange record, so a
        payload that can't be parsed fails the exchange record. The
        comparison with the stock runs in a job when
        ``stock_external_inventory_report_queue`` is installed.

        Each WMS module inherits this handler with its own name, implements
        ``_parse_payload()`` and sets its handler on its exchange type.

        :return: the result message of the processing: the warehouse, the
            report and whether its comparison is done or scheduled
        """
        payload = self._decode_payload(exchange_record)
        report_vals, lines_vals = self._parse_payload(exchange_record, payload)
        report = self._create_report(exchange_record, report_vals, lines_vals)
        report.process_comparisons_and_alerts()
        return self._get_process_message(report)

    def _get_process_message(self, report):
        """Return the result message of the processing of ``report``."""
        if report.comparison_date:
            return self.env._(
                "WH %(warehouse)s / %(report)s done",
                warehouse=report.warehouse_id.name,
                report=report.name,
            )
        return self.env._(
            "WH %(warehouse)s / %(report)s scheduled",
            warehouse=report.warehouse_id.name,
            report=report.name,
        )

    def _decode_payload(self, exchange_record):
        """Return the payload of the exchange record (JSON by default)."""
        content = exchange_record._get_file_content()
        return json.loads(content) if content else None

    def _parse_payload(self, exchange_record, payload):
        """Return the report values and the lines values of a WMS payload.

        :param exchange_record: the ``edi.exchange.record`` received
        :param payload: the decoded payload, see ``_decode_payload()``
        :return: a tuple ``(report_vals, lines_vals)``; ``report_vals`` may
            leave ``external_reference`` out, the exchange record's identifier
            is used then
        """
        raise NotImplementedError()

    def _create_report(self, exchange_record, report_vals, lines_vals):
        """Create the report of ``exchange_record`` for its backend's warehouse.

        :param exchange_record: the ``edi.exchange.record`` received
        :param report_vals: values of the report, see ``_parse_payload()``
        :param lines_vals: list of values of the report lines
        :return: the new report
        """
        backend = exchange_record.backend_id
        vals = dict(
            report_vals, backend_id=backend.id, warehouse_id=backend.warehouse_id.id
        )
        if not vals.get("external_reference"):
            vals["external_reference"] = exchange_record.identifier
        vals["line_ids"] = [Command.create(line_vals) for line_vals in lines_vals]
        report = self.env["stock.external.inventory.report"].create(vals)
        exchange_record._set_related_record(report)
        return report
