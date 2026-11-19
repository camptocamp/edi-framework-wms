# Copyright 2026 Camptocamp SA
# @author Hadrien Huvelle <hadrien.huvelle@camptocamp.com>
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "EDI WMS Stock Inventory",
    "summary": "Receive the inventory reports of a WMS through EDI",
    "version": "19.0.1.0.0",
    "category": "EDI",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/edi-framework-wms",
    "license": "AGPL-3",
    "maintainers": ["simahawk"],
    "depends": [
        "edi_core_oca",
        "edi_wms_oca",
        "stock_external_inventory_report",
    ],
    "data": [
        "views/stock_external_inventory_report_views.xml",
    ],
    "installable": True,
}
