# Right Developers Content Engine

This is a provider-free, domain-specific content engine for Right Developers and Investment Group Inc. It adapts stable architectural patterns from the RunRate Advisory engine while keeping mineral-supply strategy, evidence rules, buyer-readiness logic, and commercial routing independent.

The engine's core worldview is **Trade Readiness**:

```text
Trade Readiness
├── Buyer Readiness
├── Assay Before Terms
├── Commercial Gates
└── Specification -> Terms
```

The engine recommends and validates content packages. It does not publish, message buyers, create offers, or conduct transactions.

Run the provider-free tests with:

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -p "test_*.py" -v
```
