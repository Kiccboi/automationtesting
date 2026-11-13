# ShopFlow QA Challenge: Detailed Task Guide

This is the full list of what to do, in order. Each task matches a GitHub issue with the same number.
For every task you get:

- **Goal:** why the task exists
- **Steps:** what to do
- **Done when:** the checklist your pull request must meet
- **Git practice:** the commands this task is designed to exercise
- **Skills:** which resume skills it proves

Plan for about **4 weeks part-time**:

| Week | Tasks |
|---|---|
| 1 | Task 0 – Task 3 |
| 2 | Task 4 – Task 7 |
| 3 | Task 8 – Task 11 |
| 4 | Task 12 and the final walkthrough |

> **Rules for the whole project**
> - One task = one branch = one pull request. Never commit straight to `main`.
> - Name branches `feature/<issue-number>-<short-name>`, for example `feature/2-page-objects`.
> - The PR description must say `Closes #<issue-number>` and explain how you tested it.
> - No `time.sleep()` in tests. Use explicit waits or polling helpers.
> - Never commit `.db` files, `.venv/`, reports, or secrets.
> - Build everything against `main`. Touch `release/v1.1` only in Task 12.

---

## Task 0 — Set up your machine (no issue, do this first)

**Goal:** Get the app running locally and learn the basics of the repository.

**Steps**
1. Install **Python 3.11+**, **Git**, **Google Chrome**, **Node.js 18+** (for Newman), **Postman**,
   and optionally **Docker Desktop** and **VS Code** or **PyCharm**.
2. Configure Git with your own identity:
   ```bash
   git config --global user.name  "Aarthi Kanuganti"
   git config --global user.email "<your-github-email>"
   ```
3. Clone the repo and run the app:
   ```bash
   git clone https://github.com/Kiccboi/automationtesting.git
   cd automationtesting
   python -m venv .venv
   .venv\Scripts\activate             # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --port 8000
   ```
4. Use the app by hand at http://localhost:8000:
   - Register.
   - Add items to the cart and try the coupons.
   - Place an order with card `4242424242424242`, and another with `4000000000000002`.
   - Cancel an order.
5. Open http://localhost:8000/docs (Swagger) and call a few endpoints.
6. Read `README.md`, `docs/USER_STORIES.md` and `docs/CONTRIBUTING.md` from start to finish.
7. Explore the history and create the first release tag:
   ```bash
   git branch -a
   git log --oneline --graph --all
   git tag -a v1.0.0 -m "ShopFlow v1.0.0 baseline" <commit-sha-of-main>
   git push origin v1.0.0
   ```

**Done when**
- [ ] The app runs locally and you have placed at least one order by hand.
- [ ] Tag `v1.0.0` is visible on GitHub.
- [ ] You have written down 5 questions or assumptions about the requirements. Bring them to your first review.

**Git practice:** `config`, `clone`, `branch -a`, `log --graph`, `tag`, `push <tag>`

---

## Task 1 — Framework skeleton

**Goal:** Lay down a clean, scalable test project that every later task plugs into.

**Steps**
1. Create a branch: `git checkout -b feature/1-framework-skeleton`.
2. Create this layout:
   ```
   tests/ui/  tests/api/  tests/integration/
   pages/  utils/  data/  config/  reports/ (git-ignored)
   conftest.py  pytest.ini  requirements-test.txt
   ```
3. Add these to `requirements-test.txt`:
   - `selenium`, `pytest`, `requests`, `pytest-html`, `pytest-xdist`, `pytest-rerunfailures`
   - optionally `allure-pytest`
4. Add `config/` with environment settings: base URL, admin key, browser, headless flag and timeouts.
   Select the environment with an env var or CLI option, for example `pytest --env=local`.
5. Write a **driver factory** in `utils/driver_factory.py`:
   - Chrome, with headless on or off.
   - Window size.
   - Implicit wait set to 0. Use explicit waits only.
   - Optionally Firefox.
6. In `conftest.py`, add:
   - a `driver` fixture (function scope) that quits the driver on teardown;
   - a `base_url` fixture;
   - a hook that takes a **screenshot on failure** and attaches it to the HTML report.
7. In `pytest.ini`, register the markers `smoke`, `regression`, `integration`, `api` and `quarantine`, and set default options:
   ```
   addopts = -ra --html=reports/report.html --self-contained-html
   ```
8. Add one placeholder test that opens the home page and checks the title. Run it.

**Done when**
- [ ] `pytest -m smoke` runs and passes, and produces `reports/report.html`.
- [ ] A deliberately broken test produces a screenshot in the report.
- [ ] Headless can be switched without code changes.
- [ ] The PR has been reviewed and merged.

**Git practice:** `checkout -b`, `add -p` (stage in parts), `commit`, `push -u`, open a PR, update `.gitignore`

**Skills:** Python, Pytest, framework design

---

## Task 2 — Page objects

**Goal:** Put every locator and page interaction in one place, so tests read like business steps.

**Steps**
1. Create a `BasePage` with these methods:
   - `open(path)`
   - `find(locator)` and `click(locator)`, both with an explicit wait for clickability
   - `type(locator, text)`, which clears the field first
   - `text_of(locator)`
   - `is_visible(locator)`
   - `wait_for_url_contains(fragment)`
2. Create one class per page:
   - `LoginPage`
   - `RegisterPage`
   - `CatalogPage` (search, filter, product cards)
   - `ProductPage`
   - `CartPage`
   - `CheckoutPage` (region, shipping, coupon, card, "Update totals", "Place order", reading the quote table)
   - `OrderPage`
   - `OrderHistoryPage`
   - a `NavBar` component
3. Use the `data-testid` attributes for locators, through a helper such as `by_testid("login-email")`.
4. Page methods return the **next page object** where navigation happens, for example
   `LoginPage.login(...) -> CatalogPage`.
5. Return money as a number (cents or `Decimal`), not as `"$1,005.70"`. Write a small parser in `utils/money.py`.
6. Write UI tests for US-1 (register and login, duplicate email, wrong password), US-2 (search and filter, out of stock) and US-3 (add to cart, remove, quantity above stock).

**Done when**
- [ ] No `By.` or locator strings appear anywhere under `tests/`.
- [ ] No `time.sleep` anywhere.
- [ ] There are at least 10 UI tests, all passing on `main`.
- [ ] Adding a new page needs only a new class. Nothing else changes.

**Git practice:** small commits per page, `git diff --staged`, address review comments with follow-up commits

**Skills:** Selenium WebDriver, POM, functional testing

---

## Task 3 — API client and test-data seeding

**Goal:** Stop using the UI to create test data. Set up state quickly and reliably through the API.

**Steps**
1. Write `utils/api_client.py`, a thin wrapper over `requests.Session` with these methods:
   - `register`, `login` (stores the token), `me`
   - `add_to_cart`, `quote`, `checkout`
   - `get_order`, `cancel`, `refund`, `outbox`
   - `admin_create_product`, `admin_set_stock`, `admin_set_tier`
2. Write a data factory that produces unique emails and SKUs using uuid or a timestamp.
3. Add these fixtures:
   - `api` (anonymous client)
   - `new_user` (registered and logged in; returns email, password and client)
   - `gold_user`
   - `product_factory(price_cents, stock)`
   - `logged_in_driver` (injects the auth cookie, so UI tests skip the login screen)
4. Write a polling helper:
   ```python
   wait_until(lambda: api.get_order(id)["status"] == "PAID", timeout=5)
   ```
   This is needed because payment results arrive asynchronously.
5. Refactor the Task 2 tests to use the fixtures where possible.

**Done when**
- [ ] UI tests start on the page under test, with no clicking through setup.
- [ ] Tests do not depend on each other or on run order. Prove it with `pytest -p no:randomly` and `pytest -p randomly` (install `pytest-randomly`).
- [ ] The full UI suite runtime is noted, before and after this task, in the PR.

**Git practice:** `git stash` / `git stash pop` (park unfinished work), `git pull --rebase` before pushing

**Skills:** Python, API integration, test-data management

---

## Task 4 — Data-driven pricing tests

**Goal:** Prove the pricing rules in US-4 hold for every combination, without writing a test per case.

**Steps**
1. Create `data/pricing_cases.json` or a CSV. Each row holds:
   - case id
   - items (price × qty)
   - region
   - shipping method
   - user tier
   - coupon
   - **expected subtotal, discount, tax, shipping and total**, which you calculate yourself from the rules in US-4
2. Cover at least **25 cases**:
   - all 3 regions
   - both shipping methods
   - standard and gold tiers
   - every coupon, with and without one
   - **boundaries**: subtotal just below, exactly at and just above each coupon minimum
   - **rounding**: prices like 3333 × 3 and 1 × 1 that force half-up rounding
   - **invalid input**: unknown coupon, exhausted coupon, bad region, empty cart
3. Write one parametrized API test (`@pytest.mark.parametrize` loaded from the file) that checks `/api/checkout/quote` against the expected values.
4. Write a UI test over a subset of about 6 cases. It checks that the checkout "Update totals" table equals the API quote, **and** that the final order total after payment equals the quote.
5. Give each case a readable test id, for example `IN-gold-SAVE10-rounding`.

**Done when**
- [ ] Adding a case means adding a row only. No code changes.
- [ ] All cases pass on `main`.
- [ ] A short note in the PR explains how you calculated the expected values. Hand-calculated or spreadsheet values are fine. Copying the app's output is **not**.

**Git practice:** resolve a merge conflict. Edit `conftest.py` on `main` through a second small PR, then rebase this branch onto it.

**Skills:** data-driven framework, functional testing, boundary-value analysis

---

## Task 5 — Order lifecycle tests

**Goal:** Cover every state an order can be in, and every transition between states.

**Steps**
1. Draw the order state diagram (PENDING → PAID / PAYMENT_FAILED → CANCELLED / REFUNDED) and add it to the PR.
2. Write tests through the API and UI for:
   - successful payment → `PAID`, a confirmation email in the outbox, stock reduced, cart emptied;
   - declined card → `PAYMENT_FAILED`, stock returned, a failure email;
   - cancelling a `PENDING` and a `PAID` order → `CANCELLED`, stock returned, email;
   - refunding a `PAID` order → `REFUNDED`;
   - **invalid transitions**, which must be rejected with 409: refund a cancelled order, cancel a refunded order, cancel twice;
   - another user's order must return 404 (US-6).
3. Check each state change in **every place it appears**: API response, `GET /api/orders/{id}`, the order page, and order history.
4. Payment is asynchronous, so use your `wait_until` helper. Never sleep.

**Done when**
- [ ] Every transition in the diagram has at least one test, positive or negative.
- [ ] Running the lifecycle suite 10 times in a row (`pytest --count=10`, using `pytest-repeat`) passes every time on `main`.

**Git practice:** `git commit --amend` (fix the last commit message before pushing), `git log -p <file>`

**Skills:** functional and regression testing, async handling

---

## Task 6 — Postman collection and Newman

**Goal:** A collection a developer could run by hand, which CI also runs automatically.

**Steps**
1. Build a collection `postman/ShopFlow.postman_collection.json` with folders for Auth, Catalog, Cart, Checkout, Orders, Webhooks and Admin.
2. Create an environment file `postman/local.postman_environment.json` with `baseUrl`, `adminKey` and `webhookSecret`.
3. Use **pre-request scripts** to generate a unique email. Use **test scripts** to:
   - save the token and order id into variables, so requests chain together;
   - assert status codes, response time under 1 second, and the response JSON **schema** (`pm.response.to.have.jsonSchema`).
4. Include these negative cases:
   - no token, a garbage token, a tampered token, and an expired token (US-1);
   - invalid payloads (missing fields, wrong types, quantity 0 or 21);
   - wrong admin key;
   - wrong webhook secret;
   - checking out twice with the same cart.
5. Run it from the command line:
   ```bash
   npm install -g newman newman-reporter-htmlextra
   newman run postman/ShopFlow.postman_collection.json -e postman/local.postman_environment.json -r cli,htmlextra
   ```

**Done when**
- [ ] More than 40 assertions, all passing on `main` from a fresh database.
- [ ] The collection runs green twice in a row without manual edits, so it is re-runnable.
- [ ] The HTML report is generated in `reports/`.

**Git practice:** review a JSON diff in a PR, use `.gitattributes` or format the JSON so diffs stay readable

**Skills:** REST API testing (Postman), negative testing

---

## Task 7 — Cross-layer integration tests

**Goal:** Prove that the UI, API, database and notifications all agree. This is system integration testing.

**Steps**
1. Write a small DB helper (`utils/db.py`) that reads `data/shopflow.db` with `sqlite3`. It is **read-only**.
2. Write tests that:
   - place an order **in the UI**, then check the API order, the `orders` and `order_items` rows, `products.stock`, and the outbox email all match;
   - cancel **through the API**, then check the DB status, the order page in the UI, order history in the UI, and stock;
   - send a **payment webhook event yourself** (`POST /api/webhooks/payment`), then check it is applied once. Sending it twice must not change anything (idempotency);
   - check that order history in the UI lists the same id, status and total as `GET /api/orders`.
3. Mark them `@pytest.mark.integration`.

**Done when**
- [ ] At least 6 integration tests, each checking at least 3 layers.
- [ ] Failure messages state which layer disagreed, for example `"DB status=PAID but API status=CANCELLED"`.

**Git practice:** `git blame app/services.py` (understand who changed what), `git show <sha>`

**Skills:** system integration testing, SQL, end-to-end thinking

---

## Task 8 — Concurrency and inventory integrity

**Goal:** Check US-5: stock never goes negative, even under load.

**Steps**
1. Create a product with **stock = 1**.
2. Create 5–10 users and put the product in each user's cart.
3. Fire all their checkouts **at the same time** using `concurrent.futures.ThreadPoolExecutor`.
4. Assert that exactly one checkout returns 201, all others return 409, and final stock is 0 (check through both the API and the DB).
5. Repeat the scenario 20 times inside the test, or use `pytest-repeat`. Race conditions do not show up every time.
6. Add a similar test for the single-use coupon `ONCE`.

**Done when**
- [ ] The test is stable and green on `main` across 20 repetitions.
- [ ] The PR explains in plain words why a race condition test must be repeated.

**Git practice:** `git cherry-pick` (bring a helper commit from another branch)

**Skills:** non-functional testing, Python threading

---

## Task 9 — Jenkins pipeline

**Goal:** The tests run automatically, and the pipeline gives a clear pass or fail.

**Steps**
1. Run Jenkins locally in Docker:
   ```bash
   docker run -p 8080:8080 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
   ```
   Install the Git, Pipeline, HTML Publisher and JUnit plugins.
2. Write a **declarative `Jenkinsfile`** in the repo with these stages:
   - `Checkout`
   - `Start app` (`docker compose up -d --build`, then wait for `/api/health`)
   - `Install deps`
   - `Smoke` (`pytest -m smoke`)
   - `API` (Newman)
   - `Regression` (only on the nightly or full run)
   - `Publish reports` (JUnit XML and HTML)
   - a `post { always { docker compose down -v } }` block for teardown
3. Add a **parameter** `SUITE = smoke | full`, and a nightly trigger (`cron('H 2 * * *')`) that runs `full`.
4. Create a Jenkins **Multibranch Pipeline** job pointing at this repo, so PR branches also run the smoke stage.
5. Make failures obvious: a red build, failing tests listed in the JUnit view, and screenshots in the HTML report.

**Done when**
- [ ] The smoke run takes **under 10 minutes**.
- [ ] Screenshots of a green build and a deliberately red build are attached to the PR.
- [ ] Running the pipeline twice in a row works, because the environment is cleaned up every time.

**Git practice:** use a protected-branch mindset (no pushing to `main`), `git revert` (undo a bad merge commit safely)

**Skills:** CI/CD (Jenkins, Git), Docker basics

---

## Task 10 — Optimization and flaky-test handling

**Goal:** Make the suite fast and trustworthy, and prove it with numbers.

**Steps**
1. **Measure first.** Record total runtime, the 10 slowest tests (`pytest --durations=10`), and the pass rate over 5 runs.
2. Run in parallel with `pytest -n auto` (pytest-xdist). Fix any test that breaks because it shares data.
3. Move setup from UI to API wherever possible. Reuse the browser per worker where it is safe.
4. **Flaky-test policy:**
   - `pytest-rerunfailures` with **at most 1 rerun**, and only in CI;
   - a test that fails, then passes on rerun, is logged as **flaky**. Investigate it. Don't ignore it;
   - repeat offenders get `@pytest.mark.quarantine` and are excluded from the gate (`-m "not quarantine"`), with a JIRA ticket linked.
5. Write the policy in `docs/FLAKY_TESTS.md`.
6. Measure again.

**Done when**
- [ ] A before/after table in the PR covers runtime, slowest tests and flake rate.
- [ ] The full suite is at least **40% faster** than the Task 3 baseline.
- [ ] Flake rate on `main` is below 2% over 20 runs.

**Git practice:** `git rebase -i` is not available in every tool, so practise `git reset --soft HEAD~3` and recommit to squash your own local commits before pushing

**Skills:** test script optimization, reliability engineering

---

## Task 11 — TestRail, JIRA and Confluence

**Goal:** Connect the automation to test management, the way it works on a real team.

**Steps**
1. **TestRail:** a free trial at testrail.com is fine.
   - Create a project with sections per user story (US-1 … US-7).
   - Write test cases with preconditions, steps and expected results. Aim for **at least 40**.
   - Store the TestRail case id on each automated test, for example `@pytest.mark.testrail("C123")`.
   - Write a small script or pytest hook that creates a **test run** and posts pass/fail results through the TestRail API after each pipeline run.
2. **Traceability matrix:** a table of user story → TestRail case → automated test → latest result. Put it in `docs/TRACEABILITY.md` or export it from TestRail.
3. **JIRA:** a free Jira Software cloud site is fine.
   - Create a Scrum board.
   - Put Tasks 1–12 in as stories and plan them into 1-week sprints.
   - Move them across the board as you work. Hold a short retro note at the end of each sprint.
4. **Confluence:** a free site is fine. Write these pages:
   - Framework architecture, with a diagram;
   - How to run the tests locally and in CI;
   - Test strategy, covering what is tested at which layer and why;
   - Defect triage guide.

**Done when**
- [ ] Every user story has at least one case, and every case is either automated or marked manual with a reason.
- [ ] A pipeline run shows up as a TestRail run automatically.
- [ ] The links to the TestRail project, JIRA board and Confluence space are in the PR description.

**Skills:** TestRail, JIRA, Confluence, Agile/Scrum, SDLC/STLC

---

## Task 12 — Release v1.1 assessment (the final exam)

**Goal:** Act as the release quality gate. Decide whether **v1.1** can ship.

**Steps**
1. Check out the release candidate on a new branch, and run your **entire** gate against it: UI, API, Newman, integration and concurrency.
   ```bash
   git fetch origin
   git checkout -b qa/release-v1.1-assessment origin/release/v1.1
   # merge or copy your test code in — e.g. git merge main  (resolve conflicts if any)
   ```
2. For **every** failure, decide whether it is a product defect or a test problem. Rerun it, and look at the API responses, DB rows and screenshots.
3. Log each real defect in **JIRA**, using the template in `.github/ISSUE_TEMPLATE/bug_report.md`. Include:
   - steps to reproduce
   - expected and actual results
   - evidence (test name, screenshot, API response, DB query)
   - severity
   - frequency (always, or intermittent: x of y runs)
4. Write a **root cause analysis** for each defect that covers:
   - the category: code, data, environment, or test;
   - the evidence that proves it;
   - the **commit that introduced it**, found with `git log`, `git diff main..release/v1.1` and, where a behaviour used to work, **`git bisect`**:
     ```bash
     git bisect start origin/release/v1.1 main
     git bisect run pytest tests/<your-test-file>.py -k <test-name>
     git bisect reset
     ```
   - a prevention step: which test, check or process change would stop it coming back.
5. Write `docs/RELEASE_v1.1_REPORT.md`, covering:
   - scope tested;
   - pass/fail summary per layer;
   - defect list with severity;
   - risks;
   - a clear **GO / NO-GO** with reasons.
6. Present it in a 20-minute walkthrough. Demo the pipeline, show two RCAs, and defend the verdict.

**Done when**
- [ ] The defects are logged with evidence and RCAs.
- [ ] At least one root cause is located with `git bisect`, with the output pasted into the RCA.
- [ ] The release report is merged into `main` through a PR.

> Don't read the commits looking for bugs before your tests have found them. The point is to show that your **tests** catch problems. Git is for confirming and locating a root cause after a test fails.

**Skills:** defect lifecycle management, RCA, regression testing, Git, communication

---

## Final deliverables checklist

- [ ] Framework (Tasks 1–3) merged into `main`
- [ ] More than 25 data-driven pricing cases (Task 4)
- [ ] Lifecycle, integration and concurrency suites (Tasks 5, 7, 8)
- [ ] Postman collection and Newman report (Task 6)
- [ ] `Jenkinsfile` with smoke and nightly stages, plus screenshots (Task 9)
- [ ] Before/after optimization metrics and a flaky-test policy (Task 10)
- [ ] TestRail project, traceability matrix, JIRA board and Confluence pages (Task 11)
- [ ] Release report with defects, RCAs and a GO/NO-GO verdict (Task 12)
- [ ] Clean Git history: feature branches, reviewed PRs, meaningful commit messages, a `v1.0.0` tag
