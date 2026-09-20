# Right Developers Content Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a provider-free, testable Right Developers content engine that adapts RunRate's stable architecture while replacing all RunRate-specific strategy and commercial logic with Trade Readiness domain behavior.

**Architecture:** Use a small Python package with configuration files as the strategy source of truth. Keep domain registries, scoring, CTA governance, validation, orchestration, history, performance observations, and production-entry controls in separate modules with explicit data contracts. Store configs as JSON-subset YAML documents so the engine can load them with the Python standard library and remain usable without external provider credentials.

**Tech Stack:** Python 3.11+, standard library, `unittest`, JSON-subset YAML configuration, Markdown documentation, JSON campaign/history artifacts.

**Spec:** `right-developers-content-engine/docs/superpowers/specs/2026-09-19-right-developers-content-engine-design.md`

## Global Constraints

- All public claims must carry `VERIFIED`, `SOURCE_REQUIRED`, `ILLUSTRATIVE`, or `UNKNOWN` evidence status.
- The engine must not invent pricing, volume, availability, origin, certification, regulatory status, customer results, or testimonials.
- The canonical conversion route is `/request-info`; no other commercial route may be generated.
- Generation and performance learning cannot mutate canonical concepts, CTA architecture, evidence policy, or compliance rules.
- Human review remains required before publishing, messaging, scheduling, or lead capture.
- No provider credentials or network calls are required for the test suite.
- The RunRate worktree must not be modified.
- Production code is written only after a corresponding failing test has been observed.

---

### Task 1: Create the engine package and repository contracts

**Files:**
- Create: `right-developers-content-engine/README.md`
- Create: `right-developers-content-engine/requirements.txt`
- Create: `right-developers-content-engine/pyproject.toml`
- Create: `right-developers-content-engine/right_developers_engine/__init__.py`
- Create: `right-developers-content-engine/right_developers_engine/errors.py`
- Create: `right-developers-content-engine/tests/test_repository_contracts.py`
- Create: `right-developers-content-engine/config/production-entry-points.yaml`
- Create: `right-developers-content-engine/.gitignore`

**Interfaces:**
- `right_developers_engine.errors.ConfigurationError` is the shared configuration failure type.
- The production-entry registry declares `daily_content_package`, `content_validation`, and `performance_observation` as canonical provider-free entry points.

- [ ] **Step 1: Write the failing test**

```python
class RepositoryContractsTests(unittest.TestCase):
    def test_canonical_entry_points_exist_and_are_provider_free(self):
        registry = load_json_subset_yaml(ROOT / "config" / "production-entry-points.yaml")
        self.assertEqual(
            set(registry["entry_points"]),
            {"daily_content_package", "content_validation", "performance_observation"},
        )
        self.assertTrue(all(item["provider_default"] == "none" for item in registry["entry_points"].values()))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_repository_contracts -v`

Expected: FAIL because the package, loader, registry, and test package do not exist.

- [ ] **Step 3: Write minimal implementation**

Create the package marker, shared error, minimal JSON-subset loader import surface, registry document, Python project metadata, and README describing the provider-free boundary.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_repository_contracts -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "chore: scaffold Right Developers content engine"
```

### Task 2: Add configuration loading and domain registries

**Files:**
- Create: `right-developers-content-engine/right_developers_engine/config_loader.py`
- Create: `right-developers-content-engine/right_developers_engine/registries.py`
- Create: `right-developers-content-engine/config/worldview.yaml`
- Create: `right-developers-content-engine/config/audiences.yaml`
- Create: `right-developers-content-engine/config/content-pillars.yaml`
- Create: `right-developers-content-engine/config/canonical-ip.yaml`
- Create: `right-developers-content-engine/config/minerals.yaml`
- Create: `right-developers-content-engine/config/franchises.yaml`
- Create: `right-developers-content-engine/tests/test_registries.py`

**Interfaces:**
- `load_json_subset_yaml(path: Path) -> dict[str, object]` loads JSON-subset YAML and rejects malformed or non-object documents.
- `load_domain_registries(config_dir: Path) -> DomainRegistries` returns immutable-ish dictionaries for worldview, audiences, pillars, concepts, minerals, and franchises.
- `DomainRegistries.concept_ids() -> set[str]` returns the approved canonical concept IDs.
- `DomainRegistries.mineral(mineral_id: str) -> dict[str, object]` returns a registered mineral or raises `ConfigurationError`.

- [ ] **Step 1: Write the failing tests**

```python
def test_registry_contains_trade_readiness_ip(self):
    registries = load_domain_registries(CONFIG_DIR)
    self.assertEqual(registries.worldview["north_star"], "More transaction-ready conversations; fewer vague inquiries.")
    self.assertIn("TRADE_READINESS", registries.concept_ids())

def test_unknown_mineral_is_rejected(self):
    registries = load_domain_registries(CONFIG_DIR)
    with self.assertRaises(ConfigurationError):
        registries.mineral("lithium")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_registries -v`

Expected: FAIL because the loader, registries, and domain config files do not exist.

- [ ] **Step 3: Write minimal implementation**

Implement the loader using `json.loads`, validate the six required documents, and add the approved Right Developers domain data. Do not include RunRate names, CTA routes, or business concepts in the new configuration.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_registries -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "feat: add Right Developers strategy registries"
```

### Task 3: Implement evidence and mineral claim validation

**Files:**
- Create: `right-developers-content-engine/right_developers_engine/claims.py`
- Create: `right-developers-content-engine/config/claim-policy.yaml`
- Create: `right-developers-content-engine/tests/test_claims.py`

**Interfaces:**
- `ClaimStatus`: `VERIFIED`, `SOURCE_REQUIRED`, `ILLUSTRATIVE`, `UNKNOWN`.
- `Claim(text: str, status: ClaimStatus, source: str | None, mineral_id: str | None)`.
- `validate_claim(claim: Claim, registries: DomainRegistries) -> ValidationResult`.
- `validate_claims(claims: list[Claim], registries: DomainRegistries) -> ValidationReport`.

- [ ] **Step 1: Write the failing tests**

```python
def test_unverified_price_claim_is_hard_failure(self):
    report = validate_claims([Claim("Zircon is available at $100 per tonne", ClaimStatus.UNKNOWN, None, "ZIRCON_SAND")], REGISTRIES)
    self.assertIn("UNSUPPORTED_COMMERCIAL_CLAIM", report.hard_failures)

def test_labeled_illustration_is_allowed(self):
    report = validate_claims([Claim("Illustrative example: a buyer may need a moisture basis", ClaimStatus.ILLUSTRATIVE, None, "ZIRCON_SAND")], REGISTRIES)
    self.assertEqual(report.hard_failures, [])

def test_monazite_sensitive_claim_requires_source(self):
    report = validate_claims([Claim("Monazite transport requirements depend on applicable rules", ClaimStatus.SOURCE_REQUIRED, None, "MONAZITE")], REGISTRIES)
    self.assertIn("SOURCE_REQUIRED", report.warnings)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_claims -v`

Expected: FAIL because claim types and validation do not exist.

- [ ] **Step 3: Write minimal implementation**

Implement status-aware validation, prohibited claim categories, source requirements, and the elevated monazite review profile. Treat missing information as a warning unless the text presents it as fact.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_claims -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "feat: add mineral claim evidence controls"
```

### Task 4: Implement buyer-readiness scoring and CTA governance

**Files:**
- Create: `right-developers-content-engine/right_developers_engine/readiness.py`
- Create: `right-developers-content-engine/right_developers_engine/cta.py`
- Create: `right-developers-content-engine/config/readiness-scoring.yaml`
- Create: `right-developers-content-engine/config/funnel-cta.yaml`
- Create: `right-developers-content-engine/tests/test_readiness_and_cta.py`

**Interfaces:**
- `InquiryProfile` fields: `mineral`, `specification`, `quantity`, `destination`, `inspection`, `documentation`, `payment_pathway`, `buyer_authority`, `intended_price`, and `technical_requirements`.
- `score_inquiry(profile: InquiryProfile) -> ReadinessScore` returns `score`, `complete_fields`, `missing_fields`, and `stage`.
- `validate_cta(stage: str, tier: int, route: str | None) -> ValidationResult`.
- Canonical route constant: `REQUEST_INFO_ROUTE = "/request-info"`.

- [ ] **Step 1: Write the failing tests**

```python
def test_complete_inquiry_reaches_qualified_conversion(self):
    result = score_inquiry(complete_profile())
    self.assertEqual(result.stage, "QUALIFIED_CONVERSION")
    self.assertGreaterEqual(result.score, 8)

def test_missing_fields_are_not_treated_as_bad_faith(self):
    result = score_inquiry(InquiryProfile(mineral="ZIRCON_SAND"))
    self.assertIn("quantity", result.missing_fields)
    self.assertNotIn("BAD_FAITH", result.flags)

def test_attention_cta_cannot_route_to_request_info(self):
    result = validate_cta("ATTENTION", 4, "/request-info")
    self.assertIn("CTA_CEILING_EXCEEDED", result.hard_failures)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_readiness_and_cta -v`

Expected: FAIL because readiness, CTA tiers, and validation do not exist.

- [ ] **Step 3: Write minimal implementation**

Implement ten readiness fields, a transparent completeness score, stage thresholds, and CTA tiers 0-4. Enforce `/request-info` as the only conversion route and apply stage ceilings.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_readiness_and_cta -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "feat: add buyer readiness scoring and CTA governance"
```

### Task 5: Implement content scoring and deterministic validation

**Files:**
- Create: `right-developers-content-engine/right_developers_engine/scoring.py`
- Create: `right-developers-content-engine/right_developers_engine/validation.py`
- Create: `right-developers-content-engine/config/content-scoring.yaml`
- Create: `right-developers-content-engine/config/validation-policy.yaml`
- Create: `right-developers-content-engine/tests/test_scoring_and_validation.py`

**Interfaces:**
- `ContentUnit` fields: `content_id`, `mineral_id`, `audience_id`, `pillar_id`, `concept_ids`, `franchise_id`, `stage`, `claims`, `cta_tier`, `cta_route`, `body`, and `platform`.
- `score_content(unit: ContentUnit, registries: DomainRegistries) -> ContentScore`.
- `validate_content(unit: ContentUnit, registries: DomainRegistries) -> ValidationReport`.
- `ValidationReport.result` is `PASS`, `WARN`, or `REJECT`.

- [ ] **Step 1: Write the failing tests**

```python
def test_generic_commodity_post_is_rejected_or_requires_revision(self):
    unit = generic_zircon_price_post()
    report = validate_content(unit, REGISTRIES)
    self.assertIn(report.result, {"WARN", "REJECT"})
    self.assertTrue(report.generic_language_flags)

def test_trade_readiness_post_with_illustrative_evidence_can_pass_review(self):
    unit = qualified_trade_readiness_post()
    report = validate_content(unit, REGISTRIES)
    self.assertEqual(report.result, "PASS")
    self.assertTrue(report.human_review_required)

def test_unknown_canonical_concept_is_rejected(self):
    unit = qualified_trade_readiness_post(concept_ids=["INVENTED_CONCEPT"])
    report = validate_content(unit, REGISTRIES)
    self.assertIn("UNKNOWN_CANONICAL_CONCEPT", report.hard_failures)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_scoring_and_validation -v`

Expected: FAIL because content contracts, scoring, and validation do not exist.

- [ ] **Step 3: Write minimal implementation**

Implement weighted scoring for trade-readiness relevance, buyer specificity, mechanism, evidence, mineral accuracy, inquiry-quality potential, differentiation, CTA fit, canonical consistency, generic-language penalty, and repetition quality. Make hard failures override scores and always require human review on PASS.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_scoring_and_validation -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "feat: add content scoring and validation gates"
```

### Task 6: Implement campaign manifests, history, performance memory, and orchestrator

**Files:**
- Create: `right-developers-content-engine/right_developers_engine/campaigns.py`
- Create: `right-developers-content-engine/right_developers_engine/history.py`
- Create: `right-developers-content-engine/right_developers_engine/performance.py`
- Create: `right-developers-content-engine/right_developers_engine/orchestrator.py`
- Create: `right-developers-content-engine/schemas/campaign-manifest.schema.yaml`
- Create: `right-developers-content-engine/schemas/campaign-history.schema.yaml`
- Create: `right-developers-content-engine/schemas/performance-observation.schema.yaml`
- Create: `right-developers-content-engine/tests/test_orchestration_and_memory.py`

**Interfaces:**
- `load_campaign_manifest(path: Path) -> CampaignManifest`.
- `append_history_entry(path: Path, entry: HistoryEntry) -> None`.
- `append_performance_observation(path: Path, observation: PerformanceObservation) -> None`.
- `generate_content_package(manifest: CampaignManifest, history: History, registries: DomainRegistries) -> ContentPackage`.
- `ContentPackage` includes thesis metadata, selected concept/franchise, platform drafts, validation report, and `human_review_required=True`.

- [ ] **Step 1: Write the failing tests**

```python
def test_orchestrator_creates_reviewable_package_without_network(self):
    package = generate_content_package(sample_manifest(), History([]), REGISTRIES)
    self.assertTrue(package.human_review_required)
    self.assertEqual(package.cta_route, "/request-info")
    self.assertIsNotNone(package.validation_report)

def test_history_append_does_not_rewrite_existing_entries(self):
    append_history_entry(path, first_entry)
    append_history_entry(path, second_entry)
    history = read_history(path)
    self.assertEqual([item.entry_id for item in history], ["one", "two"])

def test_performance_learning_returns_recommendation_without_mutating_strategy(self):
    recommendation = derive_learning_recommendation(observations)
    self.assertIn(recommendation.kind, {"evidence_lens", "format", "hook", "platform"})
    self.assertFalse(recommendation.mutates_canonical_strategy)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_orchestration_and_memory -v`

Expected: FAIL because campaign, history, performance, and orchestration modules do not exist.

- [ ] **Step 3: Write minimal implementation**

Implement manifest validation, append-only JSON history and observation storage, recent-history retrieval, deterministic franchise rotation, duplication checks, package creation, and bounded performance recommendations. Do not call external APIs.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_orchestration_and_memory -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "feat: add campaign orchestration and append-only memory"
```

### Task 7: Add benchmark fixtures and operator documentation

**Files:**
- Create: `right-developers-content-engine/benchmarks/generic-commodity-prompts.json`
- Create: `right-developers-content-engine/benchmarks/expected-outcomes.json`
- Create: `right-developers-content-engine/tests/test_benchmarks.py`
- Modify: `right-developers-content-engine/README.md`
- Create: `right-developers-content-engine/docs/operator-guide.md`
- Create: `right-developers-content-engine/docs/domain-adaptation-map.md`

**Interfaces:**
- `run_benchmark_fixture(fixture: dict, registries: DomainRegistries) -> BenchmarkResult`.
- Each benchmark result records input prompt, selected mineral/pillar/stage, evidence controls, CTA tier, hard failures, and final result.

- [ ] **Step 1: Write the failing tests**

```python
def test_zircon_pricing_prompt_becomes_specification_terms_content(self):
    result = run_benchmark_fixture(load_fixture("zircon-pricing"), REGISTRIES)
    self.assertIn("SPECIFICATION_TERMS", result.selected_concepts)
    self.assertNotIn("invented_price", result.failure_codes)

def test_monazite_prompt_requires_elevated_review(self):
    result = run_benchmark_fixture(load_fixture("monazite"), REGISTRIES)
    self.assertTrue(result.elevated_review_required)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_benchmarks -v`

Expected: FAIL because benchmark fixtures and runner do not exist.

- [ ] **Step 3: Write minimal implementation**

Add benchmark prompts for zircon pricing, monazite education, ilmenite supply, LOI requests, and critical-minerals commentary. Document the expected transformation from generic commodity content to evidence-bounded trade-readiness content.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_benchmarks -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "test: add Right Developers content benchmarks"
```

### Task 8: Run the full provider-free verification suite and finalize handoff

**Files:**
- Modify: `right-developers-content-engine/README.md`
- Create: `right-developers-content-engine/docs/verification-report.md`

- [ ] **Step 1: Run the complete test suite**

Run: `python -m unittest discover -s right-developers-content-engine/tests -p "test_*.py" -v`

Expected: all tests pass with zero external provider calls.

- [ ] **Step 2: Run repository hygiene checks**

Run: `rg -n "OPENAI_API_KEY|RUNWAYML_API_SECRET|ELEVENLABS_API_KEY|BEGIN PRIVATE KEY" right-developers-content-engine --glob '!docs/superpowers/plans/**'`

Expected: no credential values and no incomplete implementation markers.

- [ ] **Step 3: Run benchmark suite**

Run: `python -m unittest right-developers-content-engine.tests.test_benchmarks -v`

Expected: all benchmark expectations pass.

- [ ] **Step 4: Record verification evidence**

Write the exact test counts, command results, provider-free confirmation, and known limitations to `docs/verification-report.md`. State explicitly that the engine recommends content and does not publish or conduct transactions.

- [ ] **Step 5: Commit**

```powershell
git add right-developers-content-engine
git commit -m "docs: record Right Developers engine verification"
```
