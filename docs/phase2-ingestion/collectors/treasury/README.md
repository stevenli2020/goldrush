# Treasury Fiscal Data transport

`treasury_api_client.py` is a minimal public-API transport. It performs paginated
HTTPS GET requests with a descriptive user agent, limited retry handling, content
validation, exact raw-page preservation, source metadata calculation, and manifest output.

It performs no accounting transformations. Variable packages own row selection,
calculation, validation, and fallback behavior.

The optional `--fields` argument passes an explicit Fiscal Data `fields` query.
L4-008 and L4-009 share this transport while retaining separate parsers, schemas,
validation, and outputs.

```bash
python treasury_api_client.py \
  https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_3 \
  --filter 'line_code_nbr:in:(130,360)' --sort record_date \
  --fields 'record_date,record_fiscal_year,line_code_nbr,classification_desc,current_fytd_rcpt_outly_amt'
```

The API is public and requires no authentication.
