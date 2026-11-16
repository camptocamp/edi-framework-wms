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
    """The lock area of the WMS is the warehouse lock location."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env["stock.warehouse"].create(
            {"name": "Test EDI WMS Lock Warehouse", "code": "TEWL"}
        )

    def test_lock_area(self):
        """The lock area maps to the lock location, both ways."""
        lock_location = self.warehouse.wh_lock_stock_loc_id
        self.assertTrue(lock_location)
        self.assertEqual(
            self.warehouse._edi_wms_get_area_location("lock"), lock_location
        )
        self.assertEqual(
            self.warehouse._edi_wms_get_location_area(lock_location), "lock"
        )

    def test_lock_area_required(self):
        """A required lock area without lock location names the field to set."""
        self.warehouse.wh_lock_stock_loc_id = False
        self.assertFalse(self.warehouse._edi_wms_get_area_location("lock"))
        with self.assertRaisesRegex(
            UserError,
            "^No Lock Location is set on warehouse Test EDI WMS Lock Warehouse$",
        ):
            self.warehouse._edi_wms_get_area_location("lock", required=True)
