'use strict';

/**
 * Translates between Oracle's catalog representation of a column type and the
 * single readable string used in schema files.
 *
 * The catalog splits a type across five columns (DATA_TYPE, DATA_LENGTH,
 * DATA_PRECISION, DATA_SCALE, CHAR_USED); a schema file that exposed all five
 * would be unreviewable. These two functions must round-trip exactly, or a
 * freshly written schema file would diff against the database it came from.
 */

function formatType(column) {
  const type = column.dataType;

  if (/^(VARCHAR2|NVARCHAR2|CHAR|NCHAR)$/.test(type)) {
    const size = column.charUsed === 'C' ? column.charLength : column.length;
    const unit = column.charUsed === 'C' ? ' CHAR' : column.charUsed === 'B' ? ' BYTE' : '';
    return `${type}(${size}${unit})`;
  }
  if (type === 'RAW') return `RAW(${column.length})`;
  if (type === 'NUMBER') {
    if (column.precision === null || column.precision === undefined) return 'NUMBER';
    return column.scale ? `NUMBER(${column.precision},${column.scale})` : `NUMBER(${column.precision})`;
  }
  if (type === 'FLOAT' && column.precision) return `FLOAT(${column.precision})`;
  return type;
}

function parseType(text) {
  const input = String(text || '').trim().toUpperCase();
  const match = input.match(/^([A-Z0-9_ ]+?)\s*(?:\(([^)]*)\))?\s*((?:WITH|TO)\s+.*)?$/);
  if (!match) throw new Error(`Cannot understand data type "${text}".`);

  const base = match[1].trim();
  const args = (match[2] || '').trim();
  const suffix = (match[3] || '').trim();

  // Types handled below rewrite dataType to the bare base name and carry their
  // size in separate fields. Everything else — TIMESTAMP(6), INTERVAL DAY(2) TO
  // SECOND(6) — keeps its arguments inline, because that is how Oracle reports
  // them in DATA_TYPE and formatType() echoes the field back unchanged.
  const column = {
    dataType: `${base}${args ? `(${args})` : ''}${suffix ? ` ${suffix}` : ''}`.trim(),
    length: 0,
    precision: null,
    scale: null,
    charLength: 0,
    charUsed: null,
  };

  if (/^(VARCHAR2|NVARCHAR2|CHAR|NCHAR)$/.test(base)) {
    const sizeMatch = args.match(/^(\d+)\s*(CHAR|BYTE)?$/);
    if (!sizeMatch) throw new Error(`${base} needs a size, for example ${base}(200 CHAR).`);
    const size = Number(sizeMatch[1]);
    // CHAR semantics is the project default (NLS_LENGTH_SEMANTICS=CHAR), so an
    // unqualified size is treated as characters rather than bytes.
    const unit = sizeMatch[2] || 'CHAR';
    column.dataType = base;
    column.charUsed = unit === 'CHAR' ? 'C' : 'B';
    column.charLength = size;
    // Oracle reports DATA_LENGTH in bytes; AL32UTF8 allows up to 4 per character.
    column.length = unit === 'CHAR' ? size * 4 : size;
    return column;
  }

  if (base === 'RAW') {
    column.dataType = 'RAW';
    column.length = Number(args) || 0;
    return column;
  }

  if (base === 'NUMBER' || base === 'FLOAT') {
    column.dataType = base;
    column.length = 22;
    if (args) {
      const [precision, scale] = args.split(',').map((part) => part.trim());
      column.precision = precision === '*' ? null : Number(precision);
      column.scale = scale !== undefined ? Number(scale) : base === 'NUMBER' ? 0 : null;
    } else if (base === 'NUMBER') {
      column.scale = null;
    }
    return column;
  }

  const fixedWidth = { DATE: 7, 'BINARY_FLOAT': 4, 'BINARY_DOUBLE': 8, CLOB: 4000, BLOB: 4000, NCLOB: 4000, ROWID: 10 };
  column.length = fixedWidth[base] !== undefined ? fixedWidth[base] : 0;
  return column;
}

/**
 * Reduces a column to the fields that define it, so a column read from the
 * database and the same column read from a schema file compare equal.
 */
function normalizeColumn(column) {
  return {
    dataType: column.dataType,
    length: column.length || 0,
    precision: column.precision === undefined ? null : column.precision,
    scale: column.scale === undefined ? null : column.scale,
    charLength: column.charLength || 0,
    charUsed: column.charUsed || null,
    nullable: column.nullable !== false,
    default: column.default === undefined ? null : column.default,
    position: column.position || 0,
  };
}

module.exports = { formatType, parseType, normalizeColumn };
