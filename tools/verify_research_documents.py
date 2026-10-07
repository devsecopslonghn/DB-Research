"""Verify research documents and source records. Do not execute candidate software."""
import argparse,csv,hashlib,json,re,subprocess,sys
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,help='Write the current check result to this path; by default print it without changing repository evidence.')
args=parser.parse_args()
errors=[];results={}
original=json.loads((ROOT/'evidence/source-manifest.json').read_text())
extra=json.loads((ROOT/'evidence/product-model/source-manifest.json').read_text())
for name,manifest in [('original',original),('supplemental',extra)]:
    checked=0
    for key,item in manifest.items():
        directory=ROOT/item['directory']
        if not (directory/'.git').exists():continue
        checked+=1
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=directory,text=True).strip()
        status=subprocess.check_output(['git','status','--porcelain'],cwd=directory,text=True).strip()
        if head!=item['sha']:errors.append(f'{name} {key}: HEAD mismatch')
        if status:errors.append(f'{name} {key}: source working tree changed: {status[:100]}')
    results[name+'_git_snapshots_checked']=checked
for filename in ['evidence/source-references.json','evidence/product-model/source-references.json']:
    refs=json.loads((ROOT/filename).read_text())
    for ref in refs:
        if 'local_path' in ref:path=ROOT/ref['local_path']
        else:
            matches=[x for x in original.values() if x['repo']==ref['repo'] and x['sha']==ref['sha']]
            if len(matches)!=1:errors.append('Cannot map '+ref['id']);continue
            path=ROOT/matches[0]['directory']/ref['file']
        if not path.is_file():errors.append(ref['id']+': missing file');continue
        if hashlib.sha256(path.read_bytes()).hexdigest()!=ref['sha256']:errors.append(ref['id']+': hash mismatch')
        if not 1<=ref['start']<=ref['end']<=len(path.read_text(errors='replace').splitlines()):errors.append(ref['id']+': line range invalid')
    results[filename+'_references_checked']=len(refs)
images=json.loads((ROOT/'evidence/product-model/screenshots.json').read_text())
for item in images:
    if hashlib.sha256((ROOT/item['local_path']).read_bytes()).hexdigest()!=item['sha256']:errors.append(item['local_path']+': screenshot hash mismatch')
results['screenshots_checked']=len(images)
documents=list(ROOT.glob('*.md'))+[ROOT/'poc/ORACLE-POC.md',ROOT/'evidence/product-model/SEARCH.md']
documents.extend((ROOT/'evaluation').glob('*.md'))
documents.extend((ROOT/'evaluation/research-round-2').glob('*.md'))
documents.extend((ROOT/'evaluation/research-round-2/coordinator').glob('*.md'))
links=0;tables=0
for document in documents:
    if document.name in ['brief.md','product-model-constraint.md']:continue
    lines=document.read_text().splitlines();previous_columns=None
    for number,line in enumerate(lines,1):
        if line.startswith('|'):
            count=len(re.split(r'(?<!\\)\|',line))-2
            if previous_columns is not None and count!=previous_columns:errors.append(f'{document.name}:{number}: inconsistent table columns')
            if previous_columns is None:tables+=1
            previous_columns=count
        else:previous_columns=None
    for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)',document.read_text()):
        target=match.group(1).strip('<>')
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target) or target.startswith('#'):continue
        dest=target.split('#')[0]
        if not dest:continue
        links+=1
        if not (document.parent/unquote(dest)).exists():errors.append(f'{document.name}: broken relative link: {target}')
results['relative_links_checked']=links;results['tables_checked']=tables
model=(ROOT/'PRODUCT-MODEL.md').read_text()
comparison_blocks=re.findall(r'\| Capability \| Bytebase reference \| Candidate \|\n\|---\|---\|---\|\n((?:\|.*\n)+)',model)
if len(comparison_blocks)!=10:errors.append('Expected ten serious-candidate comparison tables')
for block in comparison_blocks:
    if len(block.strip().splitlines())!=18:errors.append('Comparison does not contain 18 capabilities')
results['eighteen_capability_comparisons_checked']=len(comparison_blocks)
ui=(ROOT/'UI-EVIDENCE.md').read_text()
for name in ['Projects','Database Instances','Databases','Environments','Changes/Releases','Review/Approval','Deployment/Rollout','History','Audit','Users/Roles']:
    if ui.count('| '+name+' |')!=2:errors.append('Missing shortlisted frontend check: '+name)
results['shortlist_page_checks']=20
criteria_path=ROOT/'evaluation/criteria.csv'
with criteria_path.open(newline='') as stream:
    criteria=list(csv.DictReader(stream))
criteria=[row for row in criteria if row.get('origin','').startswith('poc/ORACLE-POC.md:')]
criteria_ids=[row.get('id','').strip() for row in criteria]
allowed_statuses={'PASS','PARTIAL','FAIL','BLOCKED','NOT_RUN','NOT RUN','SKIP','UNKNOWN'}
if len(criteria)!=45:errors.append(f'Expected 45 authoritative POC criteria rows, found {len(criteria)}')
if any(not case_id for case_id in criteria_ids):errors.append('Authoritative criteria contain an empty ID')
if len(criteria_ids)!=len(set(criteria_ids)):errors.append('Authoritative criteria contain duplicate IDs')
for row in criteria:
    for field in ('historical_result','new_run_status'):
        status=row.get(field,'').strip().upper()
        if status not in allowed_statuses:errors.append(f"{row.get('id','')}: invalid {field} status {status!r}")
plan=(ROOT/'poc/ORACLE-POC.md').read_text()
plan_statuses={}
for line in plan.splitlines():
    if not line.startswith('|'):continue
    cells=[cell.strip() for cell in line.strip().strip('|').split('|')]
    if cells and cells[0] in set(criteria_ids):plan_statuses[cells[0]]=cells[-1].upper().replace(' ','_')
plan_ids=re.findall(r'^\|\s*([A-Z][A-Z0-9]+-\d+)\s*\|',plan,re.M)
if len(plan_ids)!=45:errors.append(f'Expected 45 unique POC case IDs, found {len(plan_ids)}')
if len(plan_ids)!=len(set(plan_ids)):errors.append('POC plan contains duplicate case IDs')
if set(plan_ids)!=set(criteria_ids):errors.append('POC plan case IDs differ from authoritative criteria.csv')
for row in criteria:
    case_id=row['id'].strip()
    expected=row['historical_result'].strip().upper().replace(' ','_')
    actual=plan_statuses.get(case_id)
    if actual not in {status.replace(' ','_') for status in allowed_statuses}:
        errors.append(f'{case_id}: invalid POC plan result status {actual!r}')
    if actual!=expected:errors.append(f'{case_id}: POC result status differs from authoritative historical_result')
results['authoritative_criteria_rows']=len(criteria)
results['authoritative_criteria_unique_ids']=len(set(criteria_ids))
results['poc_case_ids']=len(plan_ids)
results['poc_case_ids_unique']=len(set(plan_ids))
results['allowed_case_statuses']=sorted(allowed_statuses)
runtime_path=ROOT/'evidence/product-model/odc-runtime-20261003.json'
if runtime_path.exists():
    runtime=json.loads(runtime_path.read_text())
    results['odc_deployment_inspected']=True
    if runtime.get('info',{}).get('version')!='4.4.1-20260116':errors.append('Unexpected ODC runtime version')
    volumes={v['name']:v['requested'] for v in runtime['volumes']}
    if volumes!={'odc-data':'5Gi','data-oceanbase-metadb-10gi':'10Gi'}:errors.append('ODC volume evidence differs from requested 5/10 GiB')
    if runtime.get('oracle_target_connected') or runtime.get('oracle_execution_run'):errors.append('Oracle execution must remain unverified')
    if len(runtime['workloads'])!=2 or any(w['ready_replicas']!=1 for w in runtime['workloads']):errors.append('ODC workload evidence is incomplete')
    def inspect_keys(value):
        if isinstance(value,dict):
            for key,item in value.items():
                if key.lower() in {'password','cookies','cookie','authorization','propertysources','privatekey'}:errors.append('Sensitive runtime field: '+key)
                inspect_keys(item)
        elif isinstance(value,list):
            for item in value:inspect_keys(item)
    inspect_keys(runtime)
    results['odc_runtime_api_checks']=len(runtime['api_checks'])
    results['odc_feature_rows']=(ROOT/'FEATURE-MATRIX.md').read_text().count('| OceanBase ODC |')
    if results['odc_feature_rows']!=6:errors.append('Expected five ODC feature rows and one evidence row')
    odc_review=json.loads((ROOT/'evidence/product-model/odc-integration-review.json').read_text())
    independent=odc_review['independent_review']
    if independent['status']!='SUCCESS' or independent['exit_code']!=0 or not independent['stderr_empty']:errors.append('ODC independent review failed')
    results['odc_independent_review_status']=independent['status']
run=json.loads((ROOT/'evidence/product-model/agy-fork-gemini.json').read_text())
if run.get('status')!='SUCCESS':errors.append('Independent research did not return SUCCESS')
if (ROOT/'evidence/product-model/agy-fork-gemini.stderr').read_text().strip():errors.append('Independent research stderr is not empty')
results['independent_run_status']=run.get('status')
before=json.loads((ROOT/'evidence/product-model/before-revision-hashes.json').read_text())
results['changed_existing_files']=[name for name,digest in before.items() if (ROOT/name).is_file() and hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest]
odc_baseline=ROOT/'evidence/product-model/before-odc-integration-hashes.json'
if odc_baseline.exists():
    before_odc=json.loads(odc_baseline.read_text())
    results['odc_changed_existing_files']=[name for name,digest in before_odc.items() if (ROOT/name).is_file() and hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest]
results['errors']=errors;results['application_tests_run']=False;results['oracle_execution_run']=False
rendered=json.dumps(results,indent=2)+'\n'
if args.output:
    destination=args.output if args.output.is_absolute() else Path.cwd()/args.output
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(rendered)
    print(f'Wrote current check result to {destination}')
else:
    sys.stdout.write(rendered)
raise SystemExit(1 if errors else 0)
