# Copyright 2026 Camptocamp SA
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


# After every module is loaded: creating a warehouse needs the columns other
# installed modules add
@tagged("post_install", "-at_install")
class TestStockWarehouse(TransactionCase):
    """The WMS stock areas map to the warehouse locations, both ways."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env["stock.warehouse"].create(
            {"name": "Test EDI WMS Warehouse", "code": "TEWW"}
        )

    def test_area_location(self):
        """The free and quality areas are the stock and quality locations."""
        self.assertEqual(
            self.warehouse._edi_wms_get_area_location("free"),
            self.warehouse.lot_stock_id,
        )
        self.assertEqual(
            self.warehouse._edi_wms_get_area_location("quality"),
            self.warehouse.wh_qc_stock_loc_id,
        )

    def test_unknown_area(self):
        """An unknown area is refused."""
        with self.assertRaisesRegex(UserError, "^Unrecognized stock type: mystery$"):
            self.warehouse._edi_wms_get_area_location("mystery")

    def test_required_area_location(self):
        """A required area without location is refused, else it is empty."""
        self.warehouse.wh_qc_stock_loc_id = False
        self.assertFalse(self.warehouse._edi_wms_get_area_location("quality"))
        with self.assertRaisesRegex(
            UserError,
            "^No location is set for the quality stock area on warehouse "
            "Test EDI WMS Warehouse$",
        ):
            self.warehouse._edi_wms_get_area_location("quality", required=True)

    def test_location_area(self):
        """A location gives its area, none for another location."""
        self.assertEqual(
            self.warehouse._edi_wms_get_location_area(self.warehouse.lot_stock_id),
            "free",
        )
        self.assertEqual(
            self.warehouse._edi_wms_get_location_area(
                self.warehouse.wh_qc_stock_loc_id
            ),
            "quality",
        )
        self.assertIsNone(
            self.warehouse._edi_wms_get_location_area(self.warehouse.view_location_id)
        )
