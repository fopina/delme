Test framework supports multiple `ruleid` in same line but it is not documented

```
$ semgrep --validate -f ./
Configuration is valid - found 0 configuration error(s), and 2 rule(s).
```

```
$ semgrep --test ./
2/2: ✓ All tests passed
No tests for fixes found.
```
