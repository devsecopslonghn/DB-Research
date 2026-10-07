# Database release validation

Result: **VALIDATED**

Static checks are lexical checks, not Oracle execution or a full SQL parser.

| Release | File | SHA-256 | SQL types | Policy findings |
| --- | --- | --- | --- | --- |
| REL-2026.10-DEMO01 | 001_create_customer_table.sql | 09d5a78bf5e17b5686e56df8624870d2be0bb4c168cb658c0a7d3afe94f1d102 | TABLE | INFO: no listed dangerous pattern |
| REL-2026.10-DEMO01 | 002_create_customer_sequence.sql | f7d0763c8ce610310b1320276aaad36083c5416ea634b4c41d9d0abebdd5f838 | SEQUENCE | INFO: no listed dangerous pattern |
| REL-2026.10-DEMO01 | 003_create_customer_index.sql | 6f6d297e90f75d07d5c916097712f783b8b31b09b9e419ec951c2a4a0641aef6 | INDEX | INFO: no listed dangerous pattern |
| REL-2026.10-DEMO01 | 004_create_customer_function.sql | 07c54e7d8105a171d9ecf6ad210903716e419d9dfb09066f3ca255d5b41b8da1 | FUNCTION | INFO: no listed dangerous pattern |
| REL-2026.10-DEMO01 | 005_create_customer_view.sql | 37b0b21e054c7d9370149903b4604b4c2bbc12742b0fd624bb96cbe12cc877bc | VIEW | INFO: no listed dangerous pattern |
| REL-2026.10-DEMO01 | 006_seed_reference_data.sql | b82e3f24b24e6ceabad4c571d564cdf294d7059af4af40fb4b3266d6b0c69991 | INSERT | INFO: no listed dangerous pattern |
| REL-2026.10-DEMO02-FAIL | 001_create_customer_region_index.sql | b83f01a3c43e504f7b7e174df6c8466d22623459d9a8bba853d1e67cfa868868 | INDEX | INFO: no listed dangerous pattern |
| REL-2026.10-DEMO02-FIX | 001_create_customer_region_index.sql | 8af6f2e891f034ee7bc131a49a5d41bb1999d1338c84ccdba272563fd6f1aa9d | PLSQL_BLOCK | REQUIRES_DBA_REVIEW:DYNAMIC_SQL@8 |
