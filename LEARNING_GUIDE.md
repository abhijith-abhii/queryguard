# QueryGuard — learning guide

## What it does

Ask bounded sales questions safely. The intended user is business analysts. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Ask for revenue by category, monthly revenue, top 3 products and order count. Inspect the actual SQL and parameters. Try a write statement and observe rejection by both planner tests and database authorizer tests.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Map supported natural-language intents to fixed query templates with bound parameters.
2. Enforce read-only access through SQLite URI mode, an authorizer allowlist, and a VM instruction budget.
3. Reject unsupported questions instead of generating arbitrary SQL that only looks plausible.

## Five interview questions

1. **What problem does this project solve, and what is its unit of work?** Explain ask bounded sales questions safely, identify business analysts as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Map supported natural-language intents to fixed query templates with bound parameters. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Enforce read-only access through SQLite URI mode, an authorizer allowlist, and a VM instruction budget. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Reject unsupported questions instead of generating arbitrary SQL that only looks plausible. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** A constrained natural-language parser, not a generative text-to-SQL model. It supports five documented business intents on a synthetic table. No joins, arbitrary schemas, multi-tenant permissions or semantic clarification dialogue. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add one parameterized date-range intent and test its boundaries and read-only execution.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated ask bounded sales questions safely using SQLite · Flask, with five supported natural-language business intents and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
