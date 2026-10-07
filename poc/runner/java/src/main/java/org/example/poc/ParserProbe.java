package org.example.poc;

import java.nio.file.Files;
import java.nio.file.Path;
import org.flywaydb.core.api.configuration.FluentConfiguration;
import org.flywaydb.core.internal.parser.ParsingContext;
import org.flywaydb.core.internal.resource.StringResource;
import org.flywaydb.database.oracle.OracleParser;

/** Offline parser evidence only: this entry point cannot connect to Oracle. */
public final class ParserProbe {
    public static void main(String[] args) throws Exception {
        for (String arg : args) {
            String sql = Files.readString(Path.of(arg));
            var parser = new OracleParser(new FluentConfiguration().placeholderReplacement(false), new ParsingContext());
            int count = 0;
            try (var statements = parser.parse(new StringResource(sql))) {
                while (statements.hasNext()) {
                    var statement = statements.next();
                    if (statement.getSql().isBlank()) { throw new IllegalStateException("Empty statement"); }
                    count++;
                }
            }
            System.out.println("PARSED=" + Path.of(arg).getFileName() + ":" + count);
        }
    }
}
