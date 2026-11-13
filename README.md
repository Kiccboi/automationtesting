# ShopFlow — QA Automation Challenge

ShopFlow is a small e-commerce app (storefront + REST API + SQLite) built to be **tested**.
You are the automation owner for the squad that ships it. Your job is to build the quality gate
that decides whether a release is safe to ship.

## Run the app

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```
or `docker compose up --build`.

- Storefront: http://localhost:8000 · API docs (Swagger): http://localhost:8000/docs
- Database file: `data/shopflow.db` (SQLite — you may query it directly for cross-layer checks)
- Reset to a clean database: `POST /api/_test/reset` with header `X-Admin-Key: admin-key`

## Handy facts for testing

| Thing | Value |
|---|---|
| Admin header (create products, set stock, set user tier) | `X-Admin-Key: admin-key` |
| Test cards | `4242424242424242` succeeds · `4000000000000002` is declined |
| Coupons | `SAVE10` (10%), `FLAT5` ($5 off, min $20), `FREESHIP` (free shipping from $50), `ONCE` (20%, single use) |
| Regions / tax | `IN` 18% · `US` 8% · `EU` 20% |
| Shipping | `standard` $5.00 · `express` $15.00 |
| User tiers | `standard` · `gold` (5% off). Set via `POST /api/admin/users/tier` |
| Payment result | Asynchronous — orders start `PENDING` and become `PAID` / `PAYMENT_FAILED` shortly after |
| Mock email | `GET /api/_test/outbox?to=<email>` |
| Webhook (to simulate gateway events) | `POST /api/webhooks/payment` with header `X-Webhook-Secret: whsec_test` |
| UI locators | Elements carry `data-testid` attributes |

Money is always integer **cents** in the API.

## Branches

| Branch | Meaning |
|---|---|
| `main` | **v1.0** — the released, stable baseline. Build your framework against this. |
| `release/v1.1` | **v1.1 release candidate.** Your gate must decide: ship or block? |

## Your deliverables

**Start here → [docs/TASKS.md](docs/TASKS.md)**: the detailed, step-by-step task guide (Task 0 to Task 12).

Read **[docs/USER_STORIES.md](docs/USER_STORIES.md)** first, then:

1. **Framework** — Python + Selenium + Pytest, Page Object Model, data-driven checkout tests,
   API-seeded test data, markers (`smoke`, `regression`, `integration`).
2. **API & integration tests** — a Postman collection run with Newman, plus UI→API→DB cross-layer checks.
3. **CI/CD** — a `Jenkinsfile`: PR smoke (< 10 min) and nightly full regression, with the app started via Docker Compose.
4. **Optimization** — parallel execution, flaky-test handling, before/after metrics.
5. **Test management** — test cases in TestRail traced to stories; results pushed per run; Confluence docs.
6. **Defects** — test **`release/v1.1`**. Log every defect in JIRA with an RCA (code, data, environment, or test?)
   and finish with a go/no-go recommendation.

Work like a real team: one branch per task, small commits, pull requests, and a review before merge.
See **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** and **[docs/ISSUES.md](docs/ISSUES.md)** for the task list.

> Ground rule: find defects **by testing**, and write the RCA from your evidence (failing tests, API
> responses, logs, DB state). Use `git log` / `git diff` / `git bisect` to confirm a root cause or to
> locate a regression — not to hunt for bugs before your tests have found them.
