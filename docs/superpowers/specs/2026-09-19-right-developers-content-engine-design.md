# Right Developers Content Engine Design

## Purpose

Build a domain-specific content engine for Right Developers and Investment Group Inc. using the proven architectural patterns from the RunRate Advisory engine without copying RunRate's positioning, terminology, commercial logic, or content assumptions.

The engine will produce evidence-bounded, platform-adapted content that improves the quality of mineral supply conversations. Its north-star outcome is:

> More transaction-ready conversations; fewer vague inquiries.

## Scope

The first implementation will include:

- Configuration-driven strategy and canonical intellectual property.
- Mineral and buyer registries.
- Campaign manifest and append-only campaign history.
- Daily orchestration lifecycle.
- Buyer-readiness and inquiry-quality scoring.
- Claim, evidence, compliance, and commercial-route validation.
- CTA governance.
- Platform output contracts for LinkedIn, Facebook, Instagram, X, newsletter, article, and short-form video briefs.
- Benchmark fixtures for generic commodity prompts.
- Performance observation storage with bounded learning outputs.
- Human approval boundaries.
- Canonical production-entry registry.
- Automated tests for strategy, validation, scoring, orchestration, history, and repository hygiene.

The first implementation will not publish content, send messages, place orders, create commercial offers, or autonomously modify canonical strategy.

## Domain Worldview

```text
Trade Readiness
├── Buyer Readiness
├── Assay Before Terms
├── Commercial Gates
└── Specification -> Terms
```

The engine treats a mineral inquiry as commercially actionable only when the relevant product specification, quantity, destination, inspection basis, documentation expectations, payment pathway, and buyer authority can be evaluated together.

## Canonical Concepts

The initial concept registry will contain exactly these concepts:

- Trade Readiness: the overarching readiness of a mineral conversation to progress toward executable terms.
- Buyer Readiness: the distinction between interest and the authority, capability, and intent required to transact.
- Assay Before Terms: technical and quality information must precede meaningful commercial alignment.
- Commercial Gates: a transaction advances only when the requirements of the next stage are satisfied.
- Specification -> Terms: grade, composition, moisture, packaging, inspection, quantity, destination, and payment conditions shape commercial terms.
- Inquiry Completeness: the minimum information needed to assess a buyer request responsibly.
- Destination Fit: the interaction between destination, logistics, documentation, inspection, and commercial feasibility.
- Inspection Before Commitment: inspection expectations should be aligned before the parties treat a conversation as executable.
- Interest Is Not Readiness: a request for price alone is not evidence of transactional capability.

New named concepts require explicit human approval and a versioned registry change.

## Audiences

Initial audience registry:

- Processors and refiners.
- Industrial manufacturers.
- Mineral traders and distributors.
- Procurement and sourcing teams.
- Downstream materials companies.
- Qualified intermediaries.

Each content unit must identify the audience, the commercial situation, the buyer's current readiness stage, and the material consequence of inaction or ambiguity.

## Content Pillars

The initial pillar mix is:

1. Buyer Readiness.
2. Assay and Specification Literacy.
3. Commercial Terms and Pricing Drivers.
4. Inspection, Documentation, and Payment Readiness.
5. Logistics and Destination Fit.
6. Mineral-Specific Education.
7. Responsible Trade and Counterparty Discipline.
8. Qualified Inquiry Conversion.

The engine may repeat the worldview but must vary evidence, persona, mineral, decision context, consequence, artifact, narrative treatment, or platform format.

## Mineral Registry

The initial registry will cover:

- Monazite.
- Zircon sand.
- Ilmenite.

Each mineral record must separate verified facts, source-required facts, illustrative examples, and unknowns. The registry must not imply availability, volume, origin, certification, price, or shipping capability unless those values are explicitly supplied and marked verified.

Monazite content requires an elevated review profile for technical, transport, radiological, regulatory, and documentation claims.

## Content Franchises

The first franchise set will include:

- The Inquiry Is Not Ready Yet.
- Assay Before Terms.
- What Changes the Conversation.
- One Mineral, Three Buyer Questions.
- Specification -> Terms.
- Commercial Gate Review.
- Destination Fit Check.
- Inspection Before Commitment.
- Buyer Readiness Errors.
- From Product Interest to Actionable Inquiry.

Every franchise must define its mechanism, evidence requirement, permitted formats, variation fields, and CTA ceiling.

## Funnel and CTA Governance

CTA tiers:

```text
0  Engagement: save, reflect, discuss.
1  Self-applied value: use a checklist or buyer question.
2  Proof inspection: review a mineral brief, example, or decision aid.
3  Readiness evaluation: assess whether an inquiry is commercially complete.
4  Qualified conversion: submit a detailed mineral inquiry.
```

The canonical conversion route is the existing `/request-info` workflow. The engine may recommend that route only when the content demonstrates sufficient intent and the supplied fields support qualification. It must not invent pricing, quote promises, availability claims, booking links, or alternative commercial routes.

## Evidence and Claim Policy

Every material claim receives one of these statuses:

- `VERIFIED`: supported by an approved internal source or authoritative external source.
- `SOURCE_REQUIRED`: may be used only after a source is attached.
- `ILLUSTRATIVE`: an explicitly labeled example or hypothetical scenario.
- `UNKNOWN`: not available and prohibited from being presented as fact.

Hard failures include:

- fabricated assay, grade, volume, origin, pricing, availability, certification, customer result, or testimonial;
- unsupported regulatory, radiological, logistics, or transport claim;
- presenting an illustrative scenario as a real transaction;
- using an unverified source as proof;
- leaking internal production notes into public copy.

## Buyer-Readiness Model

The engine will score inquiry readiness across:

- Product and mineral clarity.
- Specification or assay basis.
- Intended quantity and cadence.
- Destination and delivery context.
- Inspection expectations.
- Documentation requirements.
- Payment instrument or pathway.
- Buyer authority and role.
- Intended purchase price or commercial target.
- Technical and operational fit.

The model distinguishes missing information from negative evidence. A missing field lowers completeness but does not imply bad faith or inability to transact.

## Content Scoring

Each content unit will be evaluated on a 0-5 scale across:

- Trade-readiness relevance.
- Buyer specificity.
- Commercial mechanism.
- Evidence quality.
- Mineral accuracy.
- Inquiry-quality potential.
- Differentiation.
- CTA fit.
- Canonical consistency.
- Generic-language penalty.
- Repetition quality.

Positive dimensions must meet their configured floors. Hard failures override the numerical score. A passing score recommends human review; it never authorizes publishing.

## Orchestration Lifecycle

```text
Campaign brief
  -> buyer and situation selection
  -> mineral and evidence selection
  -> trade-readiness thesis
  -> franchise and format selection
  -> platform adaptation
  -> claim, evidence, and commercial validation
  -> human review
  -> approved output package
  -> performance observation
```

The orchestrator owns sequencing, recent-history lookup, duplication prevention, rotation, validation handoff, output packaging, and history-entry drafts. It does not mutate canonical strategy or publish externally.

## Platform Output Contracts

The engine will support:

- LinkedIn: technical-commercial authority and buyer education.
- Facebook: context, discussion, and practical explanation.
- Instagram carousel: visual compression of a commercial decision or checklist.
- Instagram short-form video brief: bounded educational or scenario-driven treatment.
- X: concise commercial observation or decision question.
- Newsletter: deeper buyer-readiness explanation.
- Website article: durable, search-oriented authority asset.

Platform adaptation may change treatment and length but may not change the approved thesis, evidence status, canonical concept, or CTA ceiling.

## Performance Learning

Performance observations will be append-only and will distinguish attention signals from qualified demand signals.

Tracked downstream indicators include:

- Resource views.
- Checklist downloads.
- Product-page visits.
- Complete inquiries.
- Inquiries containing quantity, destination, specification, and intended price.
- Readiness-evaluation requests.
- Progression to commercial review.

Performance may recommend changes to evidence lenses, formats, hooks, platform emphasis, or repurposing priority. It may not automatically mutate canonical concepts, campaign sequence, CTA architecture, evidence policy, or compliance rules.

## Human Approval Boundaries

Human approval is required for:

- Canonical concept changes.
- New commercial routes.
- New mineral claims or operating claims.
- External-source acceptance for sensitive claims.
- Synthetic people or scenarios represented as proof.
- Content package approval.
- Publishing, messaging, scheduling, or lead capture.

## Repository and State Controls

The engine will maintain:

- Configuration files as source of truth.
- Campaign manifests for planned sequence.
- Append-only history for generated and reviewed content.
- A production-entry registry distinguishing canonical, experimental, pending-review, and superseded routes.
- Repository hygiene tests to prevent generated state and secrets from being treated as canonical source.

The RunRate worktree will remain untouched. Only stable architectural patterns will be reimplemented in the new Right Developers directory.

## Acceptance Criteria

The implementation is acceptable when:

1. A clean checkout contains all declared source, schemas, configs, fixtures, and tests.
2. A campaign manifest can be loaded and validated without RunRate-specific dependencies.
3. A generic commodity prompt is converted into a Right Developers trade-readiness thesis.
4. The validator rejects fabricated mineral claims and unsupported commercial assertions.
5. CTA ceilings prevent premature `/request-info` conversion asks.
6. The scoring model distinguishes buyer relevance, mineral accuracy, evidence quality, and inquiry-quality potential.
7. History and performance observations are append-only.
8. Canonical concepts cannot be mutated by generation or performance-learning code.
9. The production registry identifies the canonical orchestration and validation entry points.
10. The automated test suite passes with no external provider credentials.
11. Human review remains required before public publishing or commercial follow-up.

