PROMPT EVAL_SQLPLUS
SET DEFINE ON
DEFINE eval_value = 7
SPOOL eval-sqlplus-output.txt
SELECT &eval_value FROM DUAL;
SPOOL OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE
@eval-include.sql
@@eval-include.sql
