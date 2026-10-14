
INSERT INTO public.sys_pipeline_transform_config (
      silver_company_id
    , target_table
    , column_name
    , transform_type
    , decimal_scale
    , allow_null
    , default_fallback
    , is_pii
    , created_at
    , created_by
)
VALUES
(
      '4568456'
    , 'bronze.LegacyLedgerRecord'
    , 'entry_type'
    , 'upper'
    , null
    , false
    , ''
    , false
    , now()
    , 'joan.suarez'
)
,(
      '4568456'
    , 'bronze.LegacyLedgerRecord'
    , 'currency'
    , 'upper'
    , null
    , false
    , ''
    , false
    , now()
    , 'joan.suarez'
)
,(
      '4568456'
    , 'bronze.LegacyLedgerRecord'
    , 'reconciliation_status'
    , 'upper'
    , null
    , false
    , ''
    , false
    , now()
    , 'joan.suarez'
)
,(
      '4568456'
    , 'bronze.LegacyLedgerRecord'
    , 'account_name'
    , 'lower'
    , null
    , false
    , ''
    , false
    , now()
    , 'joan.suarez'
)
;