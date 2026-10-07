package org.example.poc;

import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.logging.Logger;
import javax.sql.DataSource;

/** Verify every actual Flyway JDBC session before even schema-history writes. */
final class GuardedDataSource implements DataSource {
    GuardedDataSource() throws ClassNotFoundException {
        Class.forName("oracle.jdbc.OracleDriver");
        DriverManager.setLoginTimeout(15);
    }

    @Override public Connection getConnection() throws SQLException {
        Connection connection = DriverManager.getConnection(required("POC_JDBC_URL"), required("POC_DB_USER"), required("POC_DB_PASSWORD"));
        try {
            String[] keys = {"POC_EXPECT_DB_NAME", "POC_EXPECT_DB_UNIQUE_NAME", "POC_EXPECT_CON_NAME",
                             "POC_EXPECT_SERVICE", "POC_DB_USER", "POC_SCHEMA", "POC_EXPECT_ORACLE_VERSION"};
            try (var statement = connection.createStatement()) {
                statement.setQueryTimeout(15);
                try (var row = statement.executeQuery("SELECT SYS_CONTEXT('USERENV','DB_NAME'), "
                    + "SYS_CONTEXT('USERENV','DB_UNIQUE_NAME'), SYS_CONTEXT('USERENV','CON_NAME'), "
                    + "SYS_CONTEXT('USERENV','SERVICE_NAME'), USER, SYS_CONTEXT('USERENV','CURRENT_SCHEMA'), "
                    + "(SELECT MAX(VERSION_FULL) FROM PRODUCT_COMPONENT_VERSION WHERE PRODUCT LIKE 'Oracle Database%') FROM DUAL")) {
                    if (!row.next()) { throw new SQLException("Missing approved database identity", "08004"); }
                    for (int i = 0; i < keys.length; i++) {
                        if (!required(keys[i]).equals(row.getString(i + 1))) {
                            throw new SQLException("Database session differs from approved target", "08004");
                        }
                    }
                }
            }
            return connection;
        } catch (Exception failure) {
            connection.close();
            if (failure instanceof SQLException sql) { throw sql; }
            throw new SQLException("Approved target configuration incomplete", "08004");
        }
    }

    private static String required(String key) throws SQLException {
        String value = System.getenv(key);
        if (value == null || value.isEmpty()) { throw new SQLException("Missing protected configuration", "08004"); }
        return value;
    }

    @Override public Connection getConnection(String user, String password) throws SQLException {
        throw new SQLException("Only protected credentials are supported", "08004");
    }
    @Override public PrintWriter getLogWriter() { return null; }
    @Override public void setLogWriter(PrintWriter ignored) { }
    @Override public int getLoginTimeout() { return 15; }
    @Override public void setLoginTimeout(int ignored) { }
    @Override public Logger getParentLogger() { return Logger.getLogger("org.example.poc"); }
    @Override public boolean isWrapperFor(Class<?> type) { return type.isInstance(this); }
    @Override public <T> T unwrap(Class<T> type) throws SQLException {
        if (type.isInstance(this)) { return type.cast(this); }
        throw new SQLException("Unsupported wrapper");
    }
}
