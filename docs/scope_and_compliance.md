# Scope and Compliance — Amar Realty Evaluation

## Objective

Build a reproducible pipeline to discover, extract, clean, validate, store, and rank prospects for Amar Realty.

## Target Micro-Markets

- Hadapsar, Pune
- Fursungi, Pune

## Open Questions

- What exactly qualifies as a prospect?
- Which public sources are permitted?
- What fields are mandatory in the final lead sheet?
- How should Location, Intent, and Recency be scored?
- What validation criteria define a clean prospect?

## Compliance Rules

- Use permitted public sources only.
- Respect applicable robots.txt rules.
- Follow the evaluation's 1.5–3 second request-delay requirement.
- Do not bypass authentication or access controls.
- Do not use paid APIs or third-party lead databases.
- Do not fabricate names, contact details, or prospect intent.
- Record source URLs, extraction timestamps, validation results, and rejection counts where applicable.

## Current Status

Day 1 — Repository setup and scope definition.

Prospect criteria, source permissions, and the final output schema remain unconfirmed. No prospect scraping has started.

## Planned Pipeline

Scope confirmation → Extraction → Cleaning and validation → Deduplication → Database loading → Lead scoring → Quality checks → Final export.
