import json
import unittest
from pathlib import Path

from poc.verifier.oracle import verify


class Cursor:
    def __init__(self, objects, errors=(), count=0):
        self.objects, self.errors, self.count = objects, errors, count
        self.queries = []

    def __enter__(self): return self
    def __exit__(self, *args): pass
    def execute(self, sql, binds):
        self.queries.append((sql, binds))
        self.sql = sql
    def fetchall(self):
        return self.objects if 'ALL_OBJECTS' in self.sql else self.errors
    def fetchone(self): return (self.count,)


class Connection:
    def __init__(self, cursor): self.fake = cursor
    def cursor(self): return self.fake


class OracleVerificationTests(unittest.TestCase):
    def setUp(self):
        self.target = {"schema": "OSS_POC_WRITER"}
        self.expected = {"objects": [{"name": "OSS_POC_INVALID", "type": "FUNCTION"}], "effects": [], "invocations": []}

    def check(self, objects, errors=()):
        self.cursor = Cursor(objects, errors)
        return verify(Connection(self.cursor), self.target, self.expected)

    def test_missing_object_or_observer_visibility_is_not_verified(self):
        self.assertEqual(self.check([])['verification_status'], 'FAILED')

    def test_invalid_dictionary_status_vetoes_success(self):
        rows = [('OSS_POC_WRITER', 'OSS_POC_INVALID', 'FUNCTION', 'INVALID')]
        self.assertEqual(self.check(rows)['verification_status'], 'INVALID')

    def test_compile_errors_veto_valid_status(self):
        rows = [('OSS_POC_WRITER', 'OSS_POC_INVALID', 'FUNCTION', 'VALID')]
        self.assertEqual(self.check(rows, [(3, 2, 'ERROR', 201)])['verification_status'], 'INVALID')
        self.assertEqual(self.cursor.queries[0][1], {'owner': 'OSS_POC_WRITER', 'name': 'OSS_POC_INVALID', 'kind': 'FUNCTION'})
        self.assertIn('TYPE=:kind', self.cursor.queries[1][0])

    def test_compile_warning_is_retained_separately(self):
        rows = [('OSS_POC_WRITER', 'OSS_POC_INVALID', 'FUNCTION', 'VALID')]
        value = self.check(rows, [(3, 2, 'WARNING', 6002)])
        self.assertEqual(value['verification_status'], 'VERIFIED')
        self.assertEqual(value['objects'][0]['diagnostics'][0][2], 'WARNING')

    def test_wrong_data_effect_fails_even_when_object_valid(self):
        self.expected['effects'] = [{'table': 'OSS_POC_DATA', 'key_column': 'ID', 'key': 42, 'expected_count': 1}]
        rows = [('OSS_POC_WRITER', 'OSS_POC_INVALID', 'FUNCTION', 'VALID')]
        self.assertEqual(self.check(rows)['verification_status'], 'FAILED')
        self.assertEqual(self.cursor.queries[-1][1], {'key': 42})


if __name__ == '__main__': unittest.main()
