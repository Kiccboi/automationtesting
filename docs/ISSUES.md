# Starter issues (work them in order; one branch + PR each)

1. **Framework skeleton** — project layout, `BasePage`, driver factory (headless option), `conftest.py`, `pytest.ini` with markers, config per environment.
2. **Page objects** — login, register, catalog, product, cart, checkout, order detail, order history.
3. **API client & data seeding fixtures** — create user/product/stock/tier through the API so UI tests start from a known state.
4. **Data-driven pricing tests** — JSON/CSV matrix: region × shipping × tier × coupon, including rounding and boundary cases. Verify UI quote == API quote == final order.
5. **Order lifecycle tests** — PENDING→PAID, declined card, cancel, refund, outbox emails, stock effects. Use proper waits (no `sleep`).
6. **Postman collection** — happy path + negative cases + schema checks + token expiry; run with Newman.
7. **Cross-layer integration tests** — UI action → API state → DB row → outbox.
8. **Concurrency & inventory test** — last-unit purchase by several users.
9. **Jenkins pipeline** — PR smoke and nightly regression stages, Docker Compose, reports archived.
10. **Optimization & flakiness** — parallel run, retry/quarantine strategy, before/after metrics.
11. **TestRail & JIRA integration** — traceability matrix, result upload per run.
12. **Release v1.1 assessment** — run the gate against `release/v1.1`, log defects with RCAs, give a go/no-go.
