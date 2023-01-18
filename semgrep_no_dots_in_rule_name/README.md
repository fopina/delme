Test framework (at least) does not expect a rule ID to contain dots

Rule validation should enforce that (and maybe have that documented?)

```
pip install -r requirements.txt
```

```
$ semgrep --validate --config ./
Configuration is valid - found 0 configuration error(s), and 2 rule(s).
```

Testing each rule isolated works:

```
$ semgrep --test ./my.rule.a.py --config ./my.rule.a.yaml
1/1: ✓ All tests passed
No tests for fixes found.
$ semgrep --test ./my.rule.b.py --config ./my.rule.b.yaml
1/1: ✓ All tests passed
No tests for fixes found.
```

Testing both does not:

```
$ semgrep --test ./
Found rule id mismatch - file=/Users/fopina/Documents/delme/semgrep_no_dots_in_rule_name/my.rule.a.py 'ruleid' annotation with no YAML rule={'my.rule.a'}
Failing due to rule id mismatch. There is a test denoted with 'ruleid: <rule name>' where the rule name does not exist or is not expected in the test file.
```
