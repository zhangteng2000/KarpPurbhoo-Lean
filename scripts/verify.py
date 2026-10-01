"""Build and audit the independent Karp--Purbhoo extraction (Python 3 stdlib only)."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / 'verification/current'
LOGS.mkdir(parents=True, exist_ok=True)
ENV = os.environ.copy()
ENV.setdefault('LEAN_NUM_THREADS', '2')

def run(args, name):
    print('Running: ' + ' '.join(args), flush=True)
    path = LOGS / name
    with path.open('w', encoding='utf-8', newline='\n') as log:
        result = subprocess.run(args, cwd=ROOT, env=ENV, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        print(path.read_text(encoding='utf-8', errors='replace')[-18000:])
        raise SystemExit('FAILED: ' + ' '.join(args))
    return path.read_text(encoding='utf-8', errors='replace')

def check_sources():
    manifest = json.loads((ROOT/'verification/source-manifest.json').read_text(encoding='utf-8'))
    entries = {item['path']: item for item in manifest['files']}
    if len(entries) != manifest['module_count']:
        raise SystemExit('Duplicate or missing source manifest entries')
    pending = manifest['root_modules'].copy()
    seen = set()
    while pending:
        module = pending.pop()
        if module in seen:
            continue
        if not module.startswith(('ModifiedCartan.', 'FewInflection.')):
            continue
        seen.add(module)
        rel = module.replace('.', '/') + '.lean'
        path = ROOT / rel
        if rel not in entries or not path.is_file():
            raise SystemExit('Missing local import: ' + module)
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entries[rel]['sha256']:
            raise SystemExit('Extracted source hash changed: ' + rel)
        imports = []
        for line in data.decode('utf-8-sig').splitlines():
            match = re.match(r'^\s*(?:public\s+)?import\s+(.*)', line)
            if match:
                imports.extend(match.group(1).split('--')[0].split())
        if imports != entries[rel]['imports']:
            raise SystemExit('Import manifest differs: ' + rel)
        pending.extend(imports)
    if {m.replace('.', '/')+'.lean' for m in seen} != set(entries):
        raise SystemExit('The manifest is not the exact local import closure')
    files = [p for name in ['ModifiedCartan','FewInflection'] for p in (ROOT/name).rglob('*.lean')]
    if {p.relative_to(ROOT).as_posix() for p in files} != set(entries):
        raise SystemExit('Unexpected or missing project source files')
    files.extend(ROOT.glob('*.lean'))
    files.extend((ROOT/'verification').glob('*.lean'))
    bad = []
    for path in files:
        for line_no, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            if re.search(r'\b(?:axiom|sorry|admit)\b', line):
                bad.append(f'{path.relative_to(ROOT)}:{line_no}: {line}')
    (LOGS/'placeholder-scan.log').write_text('\n'.join(bad), encoding='utf-8')
    if bad:
        raise SystemExit('Prohibited project source tokens:\n' + '\n'.join(bad))
    message = f'SOURCE CHECK PASSED: {len(seen)} extracted modules; hashes and import closure match.\nProject source placeholder scan passed.\n'
    (LOGS/'source-check.log').write_text(message, encoding='utf-8')
    print(message, end='')

def main():
    check_sources()
    build = run(['lake','build'], 'build.log')
    print(build.strip().splitlines()[-1])
    audit = run(['lake','env','lean','verification/AllDeclarations.lean'], 'all-declarations.log')
    print(audit.strip())
    results = run(['lake','env','lean','verification/KPResults.lean'], 'kp-results.log')
    for line in results.splitlines():
        if 'depends on axioms:' in line:
            print(line)
    if 'AUDIT PASSED:' not in audit:
        raise SystemExit('Audit did not report success')
    print('VERIFICATION PASSED: independent build, exact source extraction, complete dependency audit and KP result checks.')

if __name__ == '__main__':
    main()
