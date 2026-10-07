package org.example.poc;

import java.sql.SQLException;
import org.flywaydb.core.Flyway;
import org.flywaydb.core.internal.license.VersionPrinter;

/** Fixed OSS API boundary: no arbitrary CLI flags, clean, baseline, repair or retries. */
public final class Engine {
    public static void main(String[] args) {
        if (args.length == 1 && args[0].equals("--version")) {
            System.out.println("OSS_POC_VERSION=" + VersionPrinter.getVersion());
            return;
        }
        if (args.length != 0) { System.exit(64); }
        try {
            // Route/schema/credentials are supplied exclusively by the protected runner.
            var result = Flyway.configure()
                .dataSource(new GuardedDataSource())
                .locations("filesystem:" + required("POC_MIGRATIONS"))
                .defaultSchema(required("POC_SCHEMA"))
                .schemas(required("POC_SCHEMA"))
                .table(required("POC_HISTORY_TABLE"))
                .createSchemas(false).cleanDisabled(true).baselineOnMigrate(false)
                .placeholderReplacement(false).validateOnMigrate(true)
                .outOfOrder(false).connectRetries(0)
                .load().migrate();
            System.out.println("OSS_POC_RESULT=SUCCESS:" + result.migrationsExecuted);
        } catch (Throwable failure) {
            // Never expose exception text, URLs or arbitrary engine output as retained evidence.
            boolean sqlFailure = false;
            boolean connectionFailure = false;
            for (Throwable cause = failure; cause != null; cause = cause.getCause()) {
                if (cause instanceof SQLException sql) {
                    sqlFailure = true;
                    int code = Math.abs(sql.getErrorCode());
                    String state = sql.getSQLState();
                    connectionFailure |= (state != null && state.startsWith("08"))
                        || code == 3113 || code == 3114 || code == 3135 || code == 17002
                        || (code >= 12500 && code <= 12699);
                }
            }
            System.out.println("OSS_POC_RESULT=" + (sqlFailure && !connectionFailure ? "SQL_FAILURE" : "UNKNOWN_OUTCOME"));
            System.exit(sqlFailure && !connectionFailure ? 42 : 43);
        }
    }

    private static String required(String key) {
        String value = System.getenv(key);
        if (value == null || value.isEmpty()) { throw new IllegalStateException("Missing protected configuration"); }
        return value;
    }
}
