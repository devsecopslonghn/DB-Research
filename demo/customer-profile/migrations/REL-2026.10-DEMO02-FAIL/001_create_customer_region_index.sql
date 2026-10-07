-- Safe synthetic failure: DEV succeeds; SIT raises before CREATE INDEX.
BEGIN
  IF SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA') = 'ODC_POC_20261004_SIT' THEN
    RAISE_APPLICATION_ERROR(-20042, 'DM_CP controlled SIT failure; review a new correction release');
  END IF;
END;
/
CREATE INDEX DM_CP_CUSTOMER_REGION_IX ON DM_CP_CUSTOMER (DISPLAY_NAME);
