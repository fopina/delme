Test framework does not provide any way to test rules that are restricted to specific paths.

```
pip install -r requirements.txt
```

```
$ semgrep --validate --config ./
Configuration is valid - found 0 configuration error(s), and 1 rule(s).
```

```
$ semgrep --test ./
0/1: 1 unit tests did not pass:
--------------------------------------------------------------------------------
	✖ my-rule-a
	missed lines: [3], incorrect lines: []
	test file path: /Users/fopina/Documents/delme/semgrep_cannot_test_path_includes/my-rule-a.py


No tests for fixes found.
```

Given the current tree:

```
./my-rule-a/mymodule/views.py
./my-rule-a.py
./my-rule-a.yaml
```

I would expect either `path` to be ignore during `--test` (and `my-rule-a.py` would be scanned) or that there would be support for directories with rule name so that any structure (and file names) could be used (and `my-rule-a/mymodule/views.py` would be scanned).

### Workaround

As is, the only workaround I've found is to include the test file in the path include list (and hope it won't match any projects):

```yaml
...
    paths:
      include:
      - views.py
      - my-rule-a.thiscannotbeusedanywherebuttests.py
```
