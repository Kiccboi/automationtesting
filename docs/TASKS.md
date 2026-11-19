# ShopFlow QA Challenge: Task Guide

This guide tells you **what** to deliver for each task and the standard it must meet.
**How** you design the tests is up to you. That is what's being assessed.

Tasks 2–12 are split into **28 parts of about 2 days each**. Every part is its own GitHub issue, with its own branch and pull request. Each task's original issue (#2–#12) is the parent: it lists its parts and closes when the last part is merged. Plan for about **9 weeks**.

## Task summary

| # | Task | Parts (issues) | Week | Key outcome |
|---|---|---|---|---|
| 0 | Setup | — | 1 | App running locally; you understand every feature ✅ |
| 1 | Framework skeleton | — (#1) | 1 | A test project anyone can clone and run with one command ✅ |
| 2 | Page objects (#2) | 2.1 #14, 2.2 #15, 2.3 #16, 2.4 #17 | 2–3 | UI tests that read like business steps, with every locator kept in one place. |
| 3 | API client and test data (#3) | 3.1 #18, 3.2 #19 | 3 | Tests set up their own data through the API in seconds, and never depend on each other. |
| 4 | Data-driven pricing tests (#4) | 4.1 #20, 4.2 #21, 4.3 #22 | 3–4 | The pricing rules in US-4 are verified across many combinations, driven by one data file. |
| 5 | Order lifecycle (#5) | 5.1 #23, 5.2 #24 | 4–5 | Every order state and every allowed or forbidden transition is covered. |
| 6 | Postman collection (#6) | 6.1 #25, 6.2 #26 | 5 | An API test suite that a developer can run by hand and CI can run automatically. |
| 7 | Integration testing (#7) | 7.1 #27, 7.2 #28 | 5–6 | Proof that the UI, the API, the database and the notification outbox all agree with each other. |
| 8 | Non-functional testing (#8) | 8.1 #29, 8.2 #30 | 6 | Requirements that go beyond "does the feature work" are identified, tested and justified. |
| 9 | Jenkins pipeline (#9) | 9.1 #31, 9.2 #32, 9.3 #33 | 6–7 | The quality gate runs automatically and gives a clear pass/fail, with reports. |
| 10 | Optimization and reliability (#10) | 10.1 #34, 10.2 #35 | 7–8 | A faster and more trustworthy suite, with the improvement proven by numbers. |
| 11 | Test management (#11) | 11.1 #36, 11.2 #37, 11.3 #38 | 8–9 | Your automation is connected to the team's tools, with full traceability from requirement to result. |
| 12 | Release v1.1 assessment (#12) | 12.1 #39, 12.2 #40, 12.3 #41 | 9 | A justified, evidence-based GO / NO-GO decision for the next release. |

By the end you will have shown:

- **Python + Selenium + Pytest + POM:** Tasks 1–5
- **Data-driven testing:** Task 4
- **REST API testing with Postman:** Task 6
- **System integration testing:** Task 7
- **CI/CD with Jenkins and Git:** Task 9 and all PRs
- **Test optimization:** Task 10
- **TestRail, JIRA, Confluence, Agile/Scrum:** Task 11
- **Defect lifecycle and RCA:** Task 12

## Rules for the whole project

- New to Git and GitHub? Follow **[GITHUB_GUIDE.md](GITHUB_GUIDE.md)**. Part 2 is the routine for every part.
- One part = one issue = one branch = one pull request. Never commit straight to `main`.
- Work the parts in order. Start the next part only after the previous one is reviewed and merged.
- Always start a part from the latest `main`: `git checkout main` → `git pull` → `git checkout -b <branch>`.
- Branch names are given with each part, for example `feature/2.1-base-and-auth-pages`.
- The PR description says `Closes #<part's issue number>`. The PR for the **last part of a task** also says `Closes #<task number>`, which closes the parent task.
- Build everything against `main`. Use `release/v1.1` only in Task 12.
- Never commit `.db` files, virtual environments, generated reports or secrets.
- The requirements are in `docs/USER_STORIES.md`. If something is unclear, write down your assumption and raise it in review, as you would on a real team.
- No hard-coded sleeps (`time.sleep`) anywhere in the framework.
- Every PR must say: the command you ran; the result, for example "34 passed"; anything not finished.

---

## Task 0 — Setup (no issue)

**Key outcome:** The app runs on your machine, and you understand what it does.

**Do**
- Install the tools listed in the GitHub guide, clone the repo, and run the app as described in the README.
- Use every feature by hand: register, log in, search, filter, cart, every coupon, every region, both shipping methods, both test cards, cancel, refund and order history.
- Open the API docs at `/docs` and call at least 5 endpoints.
- Create and push the annotated tag `v1.0.0`.

**Deliverables**
- [ ] Tag `v1.0.0` visible on GitHub.
- [ ] A list of at least 5 questions or assumptions about the requirements, brought to your first review.

---

## Task 1 — Framework skeleton

**Key outcome:** A test project that anyone can clone, install and run with one command.

**Deliverables**
- [ ] Folders: `tests/ui/`, `tests/api/`, `tests/integration/`, `pages/`, `utils/`, `data/`, `config/`.
- [ ] `requirements-test.txt` listing every test dependency.
- [ ] `config/` holding the base URL, browser, headless mode and timeouts per environment. You switch environment with a command-line option or environment variable, without editing code.
- [ ] `utils/driver_factory.py` that creates the browser driver, headed or headless.
- [ ] `conftest.py` with a `driver` fixture that always closes the browser, even when a test fails.
- [ ] `pytest.ini` that registers the markers `smoke`, `regression`, `integration`, `api` and `quarantine`.
- [ ] Every run writes `reports/report.html`.
- [ ] A failing UI test attaches a screenshot to the report.
- [ ] At least one passing smoke test.
- [ ] A **"How to run the tests"** section added to the README.

**Acceptance criteria**
- `pip install -r requirements-test.txt` followed by `pytest -m smoke` works on a fresh clone.
- The PR includes a screenshot of the HTML report, with one deliberately failing test and its screenshot.

**Git practice:** `checkout -b`, `add`, `commit`, `push -u`, open a PR

---

## Task 2 — Page objects

**Key outcome:** UI tests that read like business steps, with every locator kept in one place.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 2.1 | #14 | 1–2 | `BasePage`, Login and Register page objects | 3+ UI tests for US-1 | `feature/2.1-base-and-auth-pages` |
| 2.2 | #15 | 3–4 | Product list, Product detail and navigation bar | 3+ UI tests for US-2 | `feature/2.2-catalog-pages` |
| 2.3 | #16 | 5–6 | Cart page | 3+ UI tests for US-3 | `feature/2.3-cart-page` |
| 2.4 | #17 | 7–8 | Checkout, Order detail and Order history pages, plus clean-up | 1 end-to-end test | `feature/2.4-checkout-and-order-pages` |

**Applies to every part of this task**
- Locators and waits go only in `pages/`. No `By.` and no `sleep` under `tests/`.
- Page methods describe what a user does. Methods that move to another page return that page's object. Page objects never assert.
- Each test creates its own data (for example a unique email), so tests never depend on each other.
- Commit one page object at a time, with a clear message.

### Part 2.1 — Base page and authentication pages (issue #14)

**Days 1–2 · Branch:** `feature/2.1-base-and-auth-pages`

**Deliverables**
- [ ] `pages/base_page.py`: a helper that builds a locator from a `data-testid` name, and a `BasePage` class with shared actions: open a path, find (waits until visible), click (waits until clickable), type (clears first), read text, check visibility without failing.
- [ ] `pages/login_page.py`: open, log in (returns the product list page), read the error message, read the success message.
- [ ] `pages/register_page.py`: open, register (returns the login page), read the error message.
- [ ] At least **3 UI tests** for US-1.

**Done when**
- [ ] The tests read like sentences, with no Selenium code in them.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 2.2 — Catalog pages and navigation bar (issue #15)

**Days 3–4 · Branch:** `feature/2.2-catalog-pages`

**Deliverables**
- [ ] `pages/product_list_page.py`: open, search, choose a category, get the product names shown, open a product (returns the product detail page), check whether "no results" is shown.
- [ ] `pages/product_detail_page.py`: read name, price and stock, set quantity, add to cart, check whether adding is disabled, read the error message.
- [ ] `pages/nav_bar.py`: go to Cart, Orders and Login, log out, read the logged-in user.
- [ ] At least **3 UI tests** for US-2.

**Done when**
- [ ] Prices are returned as numbers, not text like `"$89.99"`. Write a small helper for this in `utils/`.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 2.3 — Cart page (issue #16)

**Days 5–6 · Branch:** `feature/2.3-cart-page`

**Deliverables**
- [ ] `pages/cart_page.py`: open, list the items (name and quantity), read the subtotal, remove an item, check whether the cart is empty, go to checkout (returns the checkout page).
- [ ] At least **3 UI tests** for US-3.

**Done when**
- [ ] Your total across Parts 2.1–2.3 is **at least 10 UI tests**.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 2.4 — Checkout and order pages, and clean-up (issue #17)

**Days 7–8 · Branch:** `feature/2.4-checkout-and-order-pages`

**Deliverables**
- [ ] `pages/checkout_page.py`: choose region and shipping, enter a coupon, update totals, read each total, enter a card, place the order (returns the order page), read the error message.
- [ ] `pages/order_page.py`: read the order id, status and totals, cancel.
- [ ] `pages/order_history_page.py`: open, list orders, read an order's status and total.
- [ ] **1 end-to-end smoke test** that goes from login to a placed order using only page objects.
- [ ] A final tidy-up: remove duplicate code, give methods and tests clear names, and add 2–3 key tests to the `smoke` marker.

**Done when**
- [ ] All of Task 2's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 2 is done when
- [ ] There's a page object for every screen.
- [ ] There are at least 10 UI tests covering US-1, US-2 and US-3, all passing on `main` in headed and headless mode.
- [ ] Searching for `By.` and `sleep` under `tests/` finds nothing.

**Git practice:** one commit per page object, review `git diff --staged` before each commit

---

## Task 3 — API client and test data

**Key outcome:** Tests set up their own data through the API in seconds, and never depend on each other.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 3.1 | #18 | 9–10 | `utils/api_client.py` | API smoke tests | `feature/3.1-api-client` |
| 3.2 | #19 | 11–12 | Fixtures, logged-in browser, wait helper | Task 2 tests refactored | `feature/3.2-test-data-fixtures` |

**Applies to every part of this task**
- Use the Swagger page at `/docs` to learn each endpoint's request and response.

### Part 3.1 — API client (issue #18)

**Days 9–10 · Branch:** `feature/3.1-api-client`

**Deliverables**
- [ ] `utils/api_client.py`: a reusable client covering every endpoint you need: auth, products, cart, checkout, orders, admin, outbox. It stores the login token and sends it on later requests.
- [ ] A few `api`-marked smoke tests that prove the client works (for example: register then log in; list products).

**Done when**
- [ ] No test builds URLs or headers by hand; they all go through the client.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 3.2 — Test-data fixtures and wait helper (issue #19)

**Days 11–12 · Branch:** `feature/3.2-test-data-fixtures`

**Deliverables**
- [ ] Fixtures that create a user, a gold user and a product with chosen price and stock, through the API.
- [ ] A fixture that gives UI tests a logged-in browser without going through the login screen.
- [ ] A reusable "wait until a condition is true" helper for asynchronous behaviour.
- [ ] Task 2 tests refactored to use the fixtures.
- [ ] The UI suite runtime measured **before** you start this part and **after**, both stated in the PR.

**Done when**
- [ ] UI tests start on the page they test, with no clicking through setup.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 3 is done when
- [ ] Tests pass when run in random order (`pytest-randomly`) and when any single test is run on its own.
- [ ] The PR for Part 3.2 states the full UI suite runtime **before and after** this task.

**Git practice:** `stash`, `pull --rebase`

---

## Task 4 — Data-driven pricing tests

**Key outcome:** The pricing rules in US-4 are verified across many combinations, driven by one data file.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 4.1 | #20 | 13–14 | Design document and data file | 25+ cases designed | `feature/4.1-pricing-test-design` |
| 4.2 | #21 | 15–16 | Parametrized API test | All cases through the API | `feature/4.2-pricing-api-tests` |
| 4.3 | #22 | 17–18 | UI checkout test on a subset | 6+ cases through the UI | `feature/4.3-pricing-ui-tests` |

**Applies to every part of this task**
- Expected values come from the requirements, never from copying the app's output.

### Part 4.1 — Test design and test data (issue #20)

**Days 13–14 · Branch:** `feature/4.1-pricing-test-design`

**Deliverables**
- [ ] `docs/PRICING_TEST_DESIGN.md` naming the test-design techniques you used (for example equivalence partitioning, boundary value analysis, decision tables). For each technique, it says which cases came from it.
- [ ] `data/pricing_cases.json` or `.csv`: each case has an id, the inputs, and the **expected** subtotal, discount, tax, shipping and total. At least **25 cases**, including invalid-input cases.
- [ ] In the design document, show how you calculated the expected values for at least 3 cases, step by step.

**Done when**
- [ ] Every rule in US-4 is covered by at least one case.
- [ ] The PR is reviewed and merged.

### Part 4.2 — API pricing tests (issue #21)

**Days 15–16 · Branch:** `feature/4.2-pricing-api-tests`

**Deliverables**
- [ ] One parametrized test that loads every case from the data file and checks it through the API.
- [ ] Readable test ids taken from the case ids.

**Done when**
- [ ] Adding a row to the data file adds a test, with no code changes.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 4.3 — UI pricing tests (issue #22)

**Days 17–18 · Branch:** `feature/4.3-pricing-ui-tests`

**Deliverables**
- [ ] A UI test that runs at least **6** of the cases through the checkout page, using your page objects.
- [ ] A way to choose which cases also run in the UI (for example a column in the data file), without code changes.

**Done when**
- [ ] All of Task 4's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 4 is done when
- [ ] Adding a case means adding one row of data, with no code changes.
- [ ] At least 25 cases, run through the API, and at least 6 through the UI. All pass on `main`.
- [ ] Test ids are readable in the report, for example `IN-gold-SAVE10`.

**Git practice:** resolve at least one merge conflict (see the GitHub guide, Part 3)

---

## Task 5 — Order lifecycle

**Key outcome:** Every order state and every allowed or forbidden transition is covered.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 5.1 | #23 | 19–20 | State diagram, tests for allowed transitions | Every allowed transition | `feature/5.1-lifecycle-valid` |
| 5.2 | #24 | 21–22 | Negative tests, UI checks | Every forbidden transition | `feature/5.2-lifecycle-negative-ui` |

**Applies to every part of this task**
- Asynchronous results are awaited with your wait helper, not sleeps.

### Part 5.1 — Lifecycle model and valid transitions (issue #23)

**Days 19–20 · Branch:** `feature/5.1-lifecycle-valid`

**Deliverables**
- [ ] `docs/ORDER_LIFECYCLE.md` with your own state diagram drawn from the user stories. Mermaid, an image, or ASCII are all fine.
- [ ] Tests for every **allowed** transition in your diagram.

**Done when**
- [ ] Every allowed arrow in the diagram has a test.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 5.2 — Forbidden transitions and UI coverage (issue #24)

**Days 21–22 · Branch:** `feature/5.2-lifecycle-negative-ui`

**Deliverables**
- [ ] Negative tests for every **forbidden** transition in your diagram.
- [ ] UI coverage of the lifecycle, using your page objects.

**Done when**
- [ ] All of Task 5's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 5 is done when
- [ ] Every arrow in your diagram has at least one test.
- [ ] Every forbidden transition has a negative test.
- [ ] Each test is tagged with the user story it covers. All tests pass on `main`.

**Git practice:** `commit --amend`, `log -p`

---

## Task 6 — Postman collection

**Key outcome:** An API test suite that a developer can run by hand and CI can run automatically.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 6.1 | #25 | 23–24 | Collection, environment; Auth, Products, Cart folders | ~20 assertions | `feature/6.1-postman-collection` |
| 6.2 | #26 | 25–26 | Checkout, Orders, Webhooks, Admin folders; Newman | 40+ assertions total | `feature/6.2-postman-newman` |

**Applies to every part of this task**
- No hard-coded URLs or keys inside requests; use environment variables.

### Part 6.1 — Collection, environment and first folders (issue #25)

**Days 23–24 · Branch:** `feature/6.1-postman-collection`

**Deliverables**
- [ ] `postman/ShopFlow.postman_collection.json` with folders for Auth, Products and Cart.
- [ ] `postman/local.postman_environment.json`.
- [ ] Requests chained through variables (for example the login token used by later requests).

**Done when**
- [ ] The collection runs green from Postman's runner on a fresh database.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 6.2 — Remaining folders and Newman (issue #26)

**Days 25–26 · Branch:** `feature/6.2-postman-newman`

**Deliverables**
- [ ] Folders for Checkout, Orders, Webhooks and Admin.
- [ ] JSON schema checks on the main responses.
- [ ] Newman command-line run that writes an HTML report to `reports/`.
- [ ] `postman/README.md` with the Newman command and how to read the report.

**Done when**
- [ ] All of Task 6's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 6 is done when
- [ ] At least **40 assertions** in total, covering status codes, response bodies, JSON schema and response time.
- [ ] Positive and negative cases in every folder.
- [ ] `newman run …` passes on a fresh database **and** passes again straight after, with no manual edits.

---

## Task 7 — Integration testing

**Key outcome:** Proof that the UI, the API, the database and the notification outbox all agree with each other.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 7.1 | #27 | 27–28 | `utils/db.py`, design table | 3 integration tests | `feature/7.1-integration-db` |
| 7.2 | #28 | 29–30 | More flows, clear failure messages | 6+ integration tests total | `feature/7.2-integration-more` |

**Applies to every part of this task**
- The database helper is **read-only**: tests never write to the database directly.

### Part 7.1 — Database helper and first integration tests (issue #27)

**Days 27–28 · Branch:** `feature/7.1-integration-db`

**Deliverables**
- [ ] `utils/db.py`: a read-only helper for querying `data/shopflow.db`.
- [ ] `docs/INTEGRATION_TESTS.md` with a table: flow → layers checked → why this flow matters.
- [ ] The first **3** integration tests.

**Done when**
- [ ] Each test checks at least 3 layers.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 7.2 — Remaining integration tests (issue #28)

**Days 29–30 · Branch:** `feature/7.2-integration-more`

**Deliverables**
- [ ] At least **3 more** integration tests, added to the table in `docs/INTEGRATION_TESTS.md`.
- [ ] Failure messages that name the layers that disagree and their values.

**Done when**
- [ ] All of Task 7's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 7 is done when
- [ ] At least **6 integration tests**, marked `integration`, each checking at least **3 layers**.
- [ ] Each failure message names the layers that disagree and their values.
- [ ] All tests pass on `main`.

**Git practice:** `blame`, `show`

---

## Task 8 — Non-functional testing

**Key outcome:** Requirements that go beyond "does the feature work" are identified, tested and justified.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 8.1 | #29 | 31–32 | `docs/NON_FUNCTIONAL.md` | Plan approved in review | `feature/8.1-non-functional-analysis` |
| 8.2 | #30 | 33–34 | Tests for 2+ requirements | 20 repeated runs | `feature/8.2-non-functional-tests` |

### Part 8.1 — Non-functional analysis (issue #29)

**Days 31–32 · Branch:** `feature/8.1-non-functional-analysis`

**Deliverables**
- [ ] `docs/NON_FUNCTIONAL.md` covering: which requirements you treat as non-functional (quote the user story), the risk each one carries, how you will test it, and what you chose **not** to test and why.

**Done when**
- [ ] The approach is agreed in review before you write the tests.
- [ ] The PR is reviewed and merged.

### Part 8.2 — Non-functional tests (issue #30)

**Days 33–34 · Branch:** `feature/8.2-non-functional-tests`

**Deliverables**
- [ ] Tests for at least **2** of the requirements in your analysis.
- [ ] In the PR, explain how you made sure the tests are meaningful, not just green, and show the result of 20 repeated runs.

**Done when**
- [ ] All of Task 8's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 8 is done when
- [ ] Tests for at least **2** non-functional requirements.
- [ ] The tests give the same result across **20 repeated runs** on `main`.

**Git practice:** `cherry-pick`

---

## Task 9 — Jenkins pipeline

**Key outcome:** The quality gate runs automatically and gives a clear pass/fail, with reports.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 9.1 | #31 | 35–36 | Jenkins running, basic `Jenkinsfile` | Smoke tests run in Jenkins | `feature/9.1-jenkins-basic` |
| 9.2 | #32 | 37–38 | Docker Compose start/stop, Newman, published reports | Full stage list | `feature/9.2-jenkins-app-reports` |
| 9.3 | #33 | 39–40 | Suite parameter, nightly run, multibranch job | PR builds and nightly builds | `feature/9.3-jenkins-schedule` |

**Applies to every part of this task**
- Jenkins runs locally; Docker is fine. Note your setup steps in the first PR.

### Part 9.1 — Jenkins setup and first pipeline (issue #31)

**Days 35–36 · Branch:** `feature/9.1-jenkins-basic`

**Deliverables**
- [ ] Jenkins running on your machine.
- [ ] A declarative `Jenkinsfile` with stages: checkout, install dependencies, smoke tests.
- [ ] A pipeline job pointing at this repo.

**Done when**
- [ ] A Jenkins build runs your smoke tests and shows the result.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 9.2 — App lifecycle, API tests and reports (issue #32)

**Days 37–38 · Branch:** `feature/9.2-jenkins-app-reports`

**Deliverables**
- [ ] A stage that starts the app with Docker Compose and waits until it's healthy, and a step that always stops it at the end.
- [ ] A stage that runs the Newman collection.
- [ ] A regression stage.
- [ ] JUnit results and HTML reports published in Jenkins.

**Done when**
- [ ] Two builds in a row both succeed.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 9.3 — Parameters, schedule and branches (issue #33)

**Days 39–40 · Branch:** `feature/9.3-jenkins-schedule`

**Deliverables**
- [ ] A parameter to choose `smoke` or `full`; the regression stage runs only for `full`.
- [ ] A nightly scheduled `full` run.
- [ ] A Multibranch Pipeline job, so PR branches run the smoke stage.
- [ ] Screenshots of a green build and a deliberately red build.

**Done when**
- [ ] All of Task 9's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 9 is done when
- [ ] The smoke run finishes in **under 10 minutes**.
- [ ] JUnit results and HTML reports are visible in Jenkins.
- [ ] Two runs in a row both succeed, because the environment is cleaned up each time.
- [ ] Screenshots of a **green** build and a deliberately **red** build are in the final PR.

**Git practice:** `revert`

---

## Task 10 — Optimization and reliability

**Key outcome:** A faster and more trustworthy suite, with the improvement proven by numbers.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 10.1 | #34 | 41–42 | Baseline metrics, parallel execution | 30%+ faster | `feature/10.1-parallel-metrics` |
| 10.2 | #35 | 43–44 | `docs/FLAKY_TESTS.md`, quarantine marker in use | 98%+ pass rate | `feature/10.2-flaky-policy` |

### Part 10.1 — Measure and parallelize (issue #34)

**Days 41–42 · Branch:** `feature/10.1-parallel-metrics`

**Deliverables**
- [ ] `docs/METRICS.md` with the **before** numbers: total runtime, the 10 slowest tests, and pass rate over 20 runs on `main`.
- [ ] Parallel execution with `pytest-xdist`, with any tests that break in parallel fixed.

**Done when**
- [ ] The **after** runtime is added to `docs/METRICS.md`.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 10.2 — Flaky-test policy (issue #35)

**Days 43–44 · Branch:** `feature/10.2-flaky-policy`

**Deliverables**
- [ ] `docs/FLAKY_TESTS.md`: your policy for detecting, investigating, retrying and quarantining unstable tests, and when a failure must **not** be treated as flaky.
- [ ] The policy applied: retries configured as your policy says, and the `quarantine` marker excluded from the gate.
- [ ] The final pass-rate numbers added to `docs/METRICS.md`.

**Done when**
- [ ] All of Task 10's "done when" items below are met.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Task 10 is done when
- [ ] The full suite is at least **30% faster** than your Task 3 baseline.
- [ ] The pass rate on `main` is at least 98% over 20 runs.
- [ ] Any test in quarantine has a linked JIRA ticket explaining why.

**Git practice:** squash your own local commits before pushing (`reset --soft`)

---

## Task 11 — Test management

**Key outcome:** Your automation is connected to the team's tools, with full traceability from requirement to result.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 11.1 | #36 | 45–46 | TestRail project, 40+ cases | Every story covered | `feature/11.1-testrail-cases` |
| 11.2 | #37 | 47–48 | Results upload, traceability matrix | Runs appear in TestRail | `feature/11.2-testrail-integration` |
| 11.3 | #38 | 49–50 | Scrum board, Confluence pages | Team tools in place | `feature/11.3-jira-confluence` |

**Applies to every part of this task**
- Free tiers or trials of TestRail, JIRA and Confluence are fine. Put the links in each PR.

### Part 11.1 — TestRail test cases (issue #36)

**Days 45–46 · Branch:** `feature/11.1-testrail-cases`

**Deliverables**
- [ ] A TestRail project with one section per user story.
- [ ] At least **40 test cases**, each with preconditions, steps and expected result.
- [ ] Each case marked as automated (with the test name) or manual (with a reason).

**Done when**
- [ ] Every user story has at least one case.
- [ ] The PR is reviewed and merged.

### Part 11.2 — TestRail results and traceability (issue #37)

**Days 47–48 · Branch:** `feature/11.2-testrail-integration`

**Deliverables**
- [ ] Each automated test linked to its TestRail case id.
- [ ] A script or pytest hook that creates a TestRail run and posts results after each pipeline run.
- [ ] `docs/TRACEABILITY.md`: user story → TestRail case ids → automated tests → latest result.

**Done when**
- [ ] A pipeline run shows up in TestRail without manual steps.
- [ ] `pytest` passes (headed and headless where UI tests are involved).
- [ ] The PR is reviewed and merged.

### Part 11.3 — JIRA board and Confluence (issue #38)

**Days 49–50 · Branch:** `feature/11.3-jira-confluence`

**Deliverables**
- [ ] A JIRA Scrum board with the project's tasks as stories, planned into 1-week sprints, with a short retro note per sprint.
- [ ] Confluence pages for framework architecture (with a diagram), how to run the tests, test strategy, and the defect triage process.

**Done when**
- [ ] All of Task 11's "done when" items below are met.
- [ ] The PR is reviewed and merged.

### Task 11 is done when
- [ ] Every user story has at least one test case, and every test case traces to a story.
- [ ] Each pipeline run posts its results to TestRail automatically.

---

## Task 12 — Release v1.1 assessment

**Key outcome:** A justified, evidence-based GO / NO-GO decision for the next release.

| Part | Issue | Days | What you build | Target | Branch |
|---|---|---|---|---|---|
| 12.1 | #39 | 51–52 | Full suite run against `release/v1.1` | Every failure triaged | `feature/12.1-release-run` |
| 12.2 | #40 | 53–54 | JIRA defects with RCAs | Every defect logged | `feature/12.2-release-defects` |
| 12.3 | #41 | 55–56 | `docs/RELEASE_v1.1_REPORT.md`, 20-minute walkthrough | GO / NO-GO | `feature/12.3-release-report` |

**Applies to every part of this task**
- `release/v1.1` is the next release candidate. You are the release quality gate.
- Find problems by testing first. Then use Git history as your tool to confirm and locate the cause.

### Part 12.1 — Run the gate on the release candidate (issue #39)

**Days 51–52 · Branch:** `feature/12.1-release-run`

**Deliverables**
- [ ] Your full suite (UI, API, Newman, integration and non-functional) run against `release/v1.1`, with the reports attached.
- [ ] A triage list: every failure marked as a product defect or a test problem, with your reasoning.

**Done when**
- [ ] No failure is left untriaged.
- [ ] The PR is reviewed and merged.

### Part 12.2 — Defects and root cause analysis (issue #40)

**Days 53–54 · Branch:** `feature/12.2-release-defects`

**Deliverables**
- [ ] Every defect logged in JIRA following `.github/ISSUE_TEMPLATE/bug_report.md`: steps to reproduce, expected and actual results, evidence, severity, frequency.
- [ ] A root cause analysis for every defect: category (code, data, environment or test), evidence, the commit that introduced it, and how to prevent it in future.

**Done when**
- [ ] At least one root cause located with `git bisect`, with the output in the RCA.
- [ ] The PR is reviewed and merged.

### Part 12.3 — Release report and walkthrough (issue #41)

**Days 55–56 · Branch:** `feature/12.3-release-report`

**Deliverables**
- [ ] `docs/RELEASE_v1.1_REPORT.md`: scope tested, results per layer, defect list by severity, risks, and a **GO / NO-GO** recommendation with reasons.
- [ ] A **20-minute walkthrough**: demo the pipeline, present two RCAs, and defend your decision.

**Done when**
- [ ] All of Task 12's "done when" items below are met.
- [ ] The PR is reviewed and merged.

### Task 12 is done when
- [ ] Every defect is backed by evidence from a test, not from reading code.
- [ ] At least one root cause is located with `git bisect`, with the output in the RCA.
- [ ] The report is merged into `main` through a PR, and the walkthrough is done.

**Git practice:** `fetch`, `diff` between branches, `bisect`

---

## Final checklist

- [ ] Tasks 1–11 merged into `main` through reviewed pull requests
- [ ] Release report, JIRA defects and RCAs from Task 12
- [ ] Clean Git history: feature branches, meaningful commits, `v1.0.0` tag
