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

## Generate Posts

From the engine directory, run the platform generator with a campaign, mineral, buyer audience, and content stage:

```powershell
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $py -m right_developers_engine.cli `
  --campaign-id TR-CLI-001 `
  --campaign-name "Trade Readiness Foundations" `
  --mineral ZIRCON_SAND `
  --audience PROCUREMENT_TEAM `
  --stage EDUCATION `
  --franchise ASSAY_BEFORE_TERMS `
  --platforms linkedin instagram facebook `
  --output-dir outputs
```

The command writes `linkedin.md`, `instagram.md`, `facebook.md`, and `package.json` to a dated folder under `outputs/`. The metadata keeps the package in `human_review_required` status. The engine does not publish or schedule posts.
