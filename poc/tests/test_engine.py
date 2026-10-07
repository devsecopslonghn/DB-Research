import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from poc.common import Rejected, digest
from poc.runner.engine import Engine


class EngineBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.jar = self.root / 'engine.jar'; self.jar.write_bytes(b'fixture-engine')
        self.driver = self.root / 'driver.jar'; self.driver.write_bytes(b'fixture-driver')
        self.driver_policy = {'approved': True, 'sha256': digest(self.driver.read_bytes())}
        self.target = {'host':'db.invalid', 'port':1521, 'service_name':'lab.invalid', 'writer_user':'WRITER',
                       'writer_secret_env':'OSS_POC_WRITER_PASSWORD', 'schema':'WRITER', 'history_table':'oss_poc_history',
                       'database_identity':{'db_name':'LAB','db_unique_name':'LAB1','con_name':'LABPDB'}, 'oracle_version':'19.25.0.0.0'}

    def tearDown(self): self.temp.cleanup()

    def engine(self):
        with patch('poc.runner.engine.subprocess.run', return_value=subprocess.CompletedProcess([], 0, b'OSS_POC_VERSION=13.9.0\n', b'')):
            return Engine(self.jar, digest(self.jar.read_bytes()), '13.9.0', self.driver, self.driver_policy)

    def test_unapproved_proprietary_driver_never_invoked(self):
        self.driver_policy['approved'] = False
        with patch('poc.runner.engine.subprocess.run') as run, self.assertRaises(Rejected):
            Engine(self.jar, digest(self.jar.read_bytes()), '13.9.0', self.driver, self.driver_policy)
        run.assert_not_called()

    def test_engine_pin_mismatch_never_invoked(self):
        with patch('poc.runner.engine.subprocess.run') as run, self.assertRaises(Rejected):
            Engine(self.jar, '0'*64, '13.9.0', self.driver, self.driver_policy)
        run.assert_not_called()

    def test_raw_output_is_discarded_and_secret_is_not_command_argument(self):
        engine = self.engine()
        completed = subprocess.CompletedProcess([], 0, b'sensitive raw log\nOSS_POC_RESULT=SUCCESS:1\n', b'sensitive stderr')
        with patch.dict(os.environ, {'OSS_POC_WRITER_PASSWORD':'fixture-secret', 'JAVA_TOOL_OPTIONS':'hostile', 'FLYWAY_LOCATIONS':'hostile'}), \
             patch('poc.runner.engine.subprocess.run', return_value=completed) as run:
            result = engine.run(self.target, self.root)
        self.assertEqual(result['outcome'], 'SUCCESS')
        self.assertNotIn('sensitive', str(result))
        self.assertNotIn('fixture-secret', str(run.call_args.args))
        self.assertNotIn('JAVA_TOOL_OPTIONS', run.call_args.kwargs['env'])
        self.assertNotIn('FLYWAY_LOCATIONS', run.call_args.kwargs['env'])

    def test_timeout_and_skip_are_unknown(self):
        engine = self.engine()
        with patch.dict(os.environ, {'OSS_POC_WRITER_PASSWORD':'fixture-secret'}):
            with patch('poc.runner.engine.subprocess.run', side_effect=subprocess.TimeoutExpired('java', 1)):
                self.assertEqual(engine.run(self.target, self.root)['outcome'], 'UNKNOWN_OUTCOME')
            with patch('poc.runner.engine.subprocess.run', return_value=subprocess.CompletedProcess([], 0, b'OSS_POC_RESULT=SUCCESS:0\n', b'')):
                self.assertEqual(engine.run(self.target, self.root)['outcome'], 'UNKNOWN_OUTCOME')


if __name__ == '__main__': unittest.main()
