"""Verify the union of installed tests, retaining the initial failed-run evidence."""
import json, re
from pathlib import Path
root=Path(__file__).parent
latest={}
counts={}
for name in ('installed-regression','legacy-regression','ui-regression'):
    result=json.loads((root/(name+'.json')).read_text())
    rows=re.findall(r'^test\w+ \(([^)]+)\) \.\.\. (ok|ERROR|FAIL)\s*$',
                    (root/(name+'.txt')).read_text(),re.MULTILINE)
    assert len(rows)==result['tests'],(name,len(rows),result)
    if name!='installed-regression':assert result['ok'],result
    for test,status in rows:latest[test]=status
    counts[name]=result['tests']
unresolved={test:status for test,status in latest.items() if status!='ok'}
assert not unresolved,unresolved
for name in ('visual','reopen','shortcut'):
    assert json.loads((root/(name+'.json')).read_text())['ok'],name
summary=dict(ok=True,unique_installed_tests=len(latest),runs=counts,unresolved=unresolved,
             note='Six initial conversion errors were existing-destination fixture collisions; '
                  'all conversion tests were rerun in a fresh directory. Startup UI tests ran separately.',
             actual_history_click=True,fresh_reopen=True,isolated_shortcut=True)
(root/'acceptance.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
