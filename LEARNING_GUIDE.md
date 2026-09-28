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

1. **How does natural language become SQL?** A constrained deterministic grammar recognizes five supported business-question intents and selects parameterized SQL templates. It is not a general-purpose generative SQL model.

2. **Why are SQL templates safer here?** The table names, operations and query shapes are known in advance. User values become bound parameters rather than arbitrary executable SQL fragments.

3. **What protects the database if an unsafe statement slips through?** The connection is read-only and an authorizer restricts permitted tables and functions. A VM execution budget and row limit bound resource usage and output size.

4. **What happens to an unsupported question?** It produces a clear rejection instead of guessing a query. The browser retains the previous successful result and identifies it as previous output.

5. **How would you extend the interface?** Add one intent with an explicit template, parameter validation and positive/negative examples. A generative planner would require a new threat model and stronger evaluation.

## Independent exercise

Add one parameterized date-range intent and test its boundaries and read-only execution.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Built a five-intent natural-language sales interface using parameterized SQL, read-only authorization and execution limits; verified 15 correctness and rejection checks.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
