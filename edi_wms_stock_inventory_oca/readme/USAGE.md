Each WMS module inherits the processor `edi.wms.inventory.report.handler.process`
with its own name, implements `_parse_payload(exchange_record, payload)` (the
report and lines values of its payload) and sets its processor on its input
exchange type. The processor:

- decodes the file of the exchange record (`_decode_payload()`, JSON by
  default);
- creates the report for the warehouse of the backend (`_create_report()`), so
  a payload that can't be parsed fails the exchange record;
- compares the report with the stock (`process_comparisons_and_alerts()`, in
  a job when `stock_external_inventory_report_queue` is installed).

Any of these steps can be overridden by the processor of an exchange type.
