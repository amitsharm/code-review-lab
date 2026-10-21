# Code review lab

A small Python storefront app for trying code review tools on the same changes.
It uses only the Python standard library. The data and scenarios are fictional;
there are no credentials, customer data, payment integrations, or running services.

## Branches

- `main`: the starting version.
- `lab/change`: proposed changes to pricing, the quote response, and lookup paths.
- `lab/clean`: a small label-normalization refactor for comparison.

For a review, compare either lab branch with `main`. Give each tool the same
branch and requirements. Keep its first findings before sharing another tool's
results, so the tools do not influence each other. Do not merge the lab branches
while comparing tools.

## Requirements

- Money is represented in integer cents; each line total is unit price times quantity.
- Shipping is free when the subtotal is at least 5,000 cents; otherwise it costs 500 cents.
- Tenant boundaries must be checked inside the document service, even when callers
  have authenticated. A known document ID does not grant access.
- Catalog values can differ between tenants for the same item identifier.
- The existing receipt client consumes the quote API's `total_cents` field.
- Label normalization strips surrounding whitespace and lowercases text.

## Run the existing tests

```sh
python3 -m unittest -v test_smoke
```

The ordinary test suite is intentionally incomplete. Passing tests alone cannot
establish that a proposed change preserves all of the requirements. Treat this
as a learning exercise, not an accuracy benchmark or production application.
