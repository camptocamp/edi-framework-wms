# Copyright 2026 Camptocamp SA
# @author Ricardo Almeida Soares <ricardo.almeidasoares@camptocamp.com>
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.exceptions import UserError

# The stock areas a WMS splits its stock into
STOCK_AREA_FREE = "free"
STOCK_AREA_QUALITY = "quality"


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    def _edi_wms_stock_area_locations(self):
        """Return the location of each WMS stock area of the warehouse.

        Override it to add areas: e.g. ``edi_wms_lock_location_oca`` adds the
        lock area.

        :return: dict ``{area: stock.location}``; a location can be empty
            when the warehouse is not set up for that area
        """
        self.ensure_one()
        return {
            STOCK_AREA_FREE: self.lot_stock_id,
            STOCK_AREA_QUALITY: self.wh_qc_stock_loc_id,
        }

    def _edi_wms_get_area_location(self, area, required=False):
        """Return the location of the WMS stock area ``area``.

        :param area: name of the stock area
        :param required: raise if the warehouse has no location for the area
        :return: ``stock.location`` record, empty when not set up
        """
        locations = self._edi_wms_stock_area_locations()
        if area not in locations:
            raise UserError(
                self.env._("Unrecognized stock type: %(stock_type)s", stock_type=area)
            )
        location = locations[area]
        if required and not location:
            raise UserError(self._edi_wms_missing_area_location_message(area))
        return location

    def _edi_wms_missing_area_location_message(self, area):
        """Return the error raised when the warehouse has no location for ``area``."""
        return self.env._(
            "No location is set for the %(area)s stock area on warehouse %(warehouse)s",
            area=area,
            warehouse=self.display_name,
        )

    def _edi_wms_get_location_area(self, location):
        """Return the WMS stock area of ``location``, or ``None``."""
        for area, area_location in self._edi_wms_stock_area_locations().items():
            if area_location and area_location == location:
                return area
        return None
