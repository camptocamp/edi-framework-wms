# Copyright 2026 Camptocamp SA
# @author Akim Juillerat <akim.juillerat@camptocamp.com>
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models

STOCK_AREA_LOCK = "lock"


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    def _edi_wms_stock_area_locations(self):
        # OVERRIDE: the lock area is the warehouse lock location
        res = super()._edi_wms_stock_area_locations()
        res[STOCK_AREA_LOCK] = self.wh_lock_stock_loc_id
        return res

    def _edi_wms_missing_area_location_message(self, area):
        # OVERRIDE: name the field to set
        if area == STOCK_AREA_LOCK:
            return self.env._(
                "No Lock Location is set on warehouse %(warehouse)s",
                warehouse=self.display_name,
            )
        return super()._edi_wms_missing_area_location_message(area)
