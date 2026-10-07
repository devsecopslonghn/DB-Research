"""Run local safety/parser checks and append a timestamped non-Oracle evidence record."""
import io
import json
import subprocess
import unittest
from pathlib import Path

from poc.common import digest, now

ROOT = Path(__file__).resolve().parents[2]
POC = ROOT / "poc"


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cases = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.cases.append({"case_id": test.id(), "status": "PASS"})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.cases.append({"case_id": test.id(), "status": "FAIL"})

    def addError(self, test, error):
        super().addError(test, error)
        self.cases.append({"case_id": test.id(), "status": "FAIL"})


def main():
    timestamp = now()
    output = POC / "reports" / ("local-" + timestamp.replace("-", "").replace(":", "").replace("+", "_"))
    output.mkdir(parents=True, exist_ok=False)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(POC / 'tests'), pattern='test_*.py')
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=RecordedResult).run(suite)
    jar = POC / 'runner/java/target/oss-oracle-runner-1.0.0.jar'
    scripts = {'poc/fixtures/T1_function.sql':2, 'poc/fixtures/T2_invalid.sql':2,
               'poc/fixtures/T6_partial.sql':3, 'poc/fixtures/T7_lost_result.sql':2,
               'evaluation/workloads/release-small.sql':11}
    version = subprocess.run(['java', '-jar', str(jar), '--version'], capture_output=True, text=True, cwd=ROOT)
    parsed = subprocess.run(['java', '-cp', str(jar), 'org.example.poc.ParserProbe', *scripts],
                            capture_output=True, text=True, cwd=ROOT)
    observed = {line.split('=')[1].split(':')[0]: int(line.rsplit(':', 1)[1])
                for line in parsed.stdout.splitlines() if line.startswith('PARSED=')}
    parser_pass = parsed.returncode == 0 and observed == {Path(p).name:n for p,n in scripts.items()}
    data = {'timestamp': timestamp, 'scope':'LOCAL_ONLY; no Oracle connection or authenticated CI approval',
            'status':'PASS' if result.wasSuccessful() and parser_pass and version.returncode == 0 else 'FAIL',
            'tests_run':result.testsRun, 'tests':result.cases, 'test_log':'tests.log',
            'engine':'Flyway Community', 'engine_version_readback':version.stdout.strip(),
            'engine_sha256':digest(jar.read_bytes()), 'oracle_driver_bundled':False,
            'oracle_version':'UNCONFIRMED', 'parser_status':'PASS' if parser_pass else 'FAIL',
            'parser_observed_statements':observed,
            'artifacts':{p:{'sha256':digest((ROOT/p).read_bytes()),'expected_statements':n} for p,n in scripts.items()}}
    (output/'checks.json').write_text(json.dumps(data,indent=2)+'\n')
    (output/'tests.log').write_text(stream.getvalue())
    (output/'parser.log').write_text(parsed.stdout)
    print(output.relative_to(ROOT))
    return 0 if data['status']=='PASS' else 1


if __name__ == '__main__': raise SystemExit(main())
