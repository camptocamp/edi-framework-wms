- Go to *EDI > Config > Backend types* and check *WMS* on the
  backend types that connect to a WMS. Integration modules usually set it
  in their data.
- The backends of these types are *WMS Enabled*: set the *Warehouse* the
  WMS serves on each of them.

Developers can override `edi.backend._compute_wms_enabled()` to enable
the WMS features on other conditions.

The WMS modules exchange stock quantities per *stock area*: `free` (the
warehouse stock location) and `quality` (its quality control location).
Developers can add areas by overriding
`stock.warehouse._edi_wms_stock_area_locations()`, as
`edi_wms_lock_location_oca` does for the lock area.
