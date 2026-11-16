Base module for the exchanges with a warehouse management system (WMS)
through the EDI framework.

It flags the EDI backend types that connect to a WMS, and gives their
backends the warehouse the WMS serves. The WMS modules rely on the
backend's *WMS Enabled* flag to apply their rules only to the records
exchanged with a WMS.

It also maps the WMS stock areas (free stock, quality control) to the
warehouse locations, in both directions.
