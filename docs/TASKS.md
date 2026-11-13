# ShopFlow QA Challenge: Task Guide

This guide tells you **what** to deliver for each task and the standard it must meet.
**How** you design the tests is up to you. That is what's being assessed.

Each task matches a GitHub issue with the same number. Plan for about **4 weeks part-time**.

## Task summary

| # | Task | Week | Key outcome | Main deliverables |
|---|---|---|---|---|
| 0 | Setup | 1 | App running locally; you understand every feature | `v1.0.0` tag, list of questions |
| 1 | Framework skeleton | 1 | A test project anyone can clone and run with one command | `conftest.py`, `pytest.ini`, `config/`, `utils/driver_factory.py`, HTML report |
| 2 | Page objects | 1 | UI tests that read like business steps, with no locators in tests | `pages/`, 10+ UI tests |
| 3 | API client and test data | 1 | Fast, independent tests that set up their own data | `utils/api_client.py`, data fixtures, runtime before/after |
| 4 | Data-driven pricing tests | 2 | Pricing rules proven across many combinations from one data file | `data/pricing_cases.*`, 25+ cases, API and UI tests |
| 5 | Order lifecycle | 2 | Every order state and transition covered | Lifecycle diagram, lifecycle tests |
| 6 | Postman collection | 2 | An API suite developers and CI can both run | Collection, environment, 40+ assertions, Newman report |
| 7 | Integration testing | 2 | Proof that UI, API, database and notifications agree | `utils/db.py`, 6+ integration tests |
| 8 | Non-functional testing | 3 | Requirements beyond plain functionality are tested and justified | `docs/NON_FUNCTIONAL.md`, tests |
| 9 | Jenkins pipeline | 3 | Tests run automatically and give a clear pass/fail | `Jenkinsfile`, smoke and nightly runs, screenshots |
| 10 | Optimization and reliability | 3 | A faster, stable suite, proven with numbers | `docs/METRICS.md`, `docs/FLAKY_TESTS.md` |
| 11 | Test management | 3 | Automation connected to team tools, with full traceability | TestRail project, `docs/TRACEABILITY.md`, JIRA board, Confluence |
| 12 | Release v1.1 assessment | 4 | A justified GO / NO-GO decision for the next release | JIRA defects with RCAs, `docs/RELEASE_v1.1_REPORT.md`, walkthrough |

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

- New to Git and GitHub? Follow **[GITHUB_GUIDE.md](GITHUB_GUIDE.md)**. Part 2 is the routine for every task.
- One task = one branch = one pull request. Never commit straight to `main`.
- Name branches `feature/<issue-number>-<short-name>`. The PR description says `Closes #<issue-number>` and explains how you tested your work.
- Build everything against `main`. Use `release/v1.1` only in Task 12.
- Never commit `.db` files, virtual environments, generated reports or secrets.
- The requirements are in `docs/USER_STORIES.md`. If something is unclear, write down your assumption and raise it in review, as you would on a real team.
- No hard-coded sleeps (`time.sleep`) anywhere in the framework.
- Every PR must say:
  - the command you ran;
  - the result, for example "34 passed";
  - anything not finished.

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

**Deliverables**
- [ ] A `BasePage` with shared actions: open, find, click, type, read text and wait.
- [ ] A page object for every screen: Login, Register, Product list, Product detail, Cart, Checkout, Order detail, Order history, plus the navigation bar.
- [ ] At least **10 UI tests** covering US-1, US-2 and US-3.

**Acceptance criteria**
- Locators and waits appear only in `pages/`. A search for `By.` under `tests/` finds nothing.
- Page methods that navigate return the next page object.
- All UI tests pass on `main`, in both headed and headless mode.

**Git practice:** one commit per page object, review `git diff --staged` before each commit

---

## Task 3 — API client and test data

**Key outcome:** Tests set up their own data through the API in seconds, and never depend on each other.

**Deliverables**
- [ ] `utils/api_client.py` covering every endpoint you need: auth, products, cart, checkout, orders, admin, outbox.
- [ ] Fixtures that create a user, a gold user and a product with chosen price and stock.
- [ ] A fixture that gives UI tests a logged-in browser without going through the login screen.
- [ ] A reusable "wait until a condition is true" helper for asynchronous behaviour.
- [ ] Task 2 tests refactored to use the fixtures.

**Acceptance criteria**
- Tests pass when run in random order (`pytest-randomly`) and when any single test is run on its own.
- The PR states the full UI suite runtime **before and after** this task.

**Git practice:** `stash`, `pull --rebase`

---

## Task 4 — Data-driven pricing tests

**Key outcome:** The pricing rules in US-4 are verified across many combinations, driven by one data file.

**Deliverables**
- [ ] `data/pricing_cases.json` or `.csv`. Each case has an id, the inputs, and the **expected** subtotal, discount, tax, shipping and total.
- [ ] At least **25 cases**, including invalid-input cases.
- [ ] One parametrized API test that runs every case.
- [ ] A UI test that runs at least **6** of the cases through the checkout page.
- [ ] `docs/PRICING_TEST_DESIGN.md` that names the test-design techniques you used (for example equivalence partitioning, boundary value analysis, decision tables). For each technique, it explains which cases came from it and how you calculated the expected values.

**Acceptance criteria**
- Adding a case means adding one row of data, with no code changes.
- Expected values come from the requirements, never from copying the app's output.
- Test ids are readable in the report, for example `IN-gold-SAVE10`.
- All cases pass on `main`.

**Git practice:** resolve at least one merge conflict (see the GitHub guide, Part 3)

---

## Task 5 — Order lifecycle

**Key outcome:** Every order state and every allowed or forbidden transition is covered.

**Deliverables**
- [ ] `docs/ORDER_LIFECYCLE.md` with your own state diagram drawn from the user stories. Mermaid, an image, or ASCII are all fine.
- [ ] Tests for every transition in your diagram, valid and invalid, through the API and the UI.
- [ ] Each test is tagged with the user story it covers.

**Acceptance criteria**
- Every arrow in your diagram has at least one test.
- Every forbidden transition has a negative test.
- Asynchronous results are awaited with your wait helper, not sleeps.
- All tests pass on `main`.

**Git practice:** `commit --amend`, `log -p`

---

## Task 6 — Postman collection

**Key outcome:** An API test suite that a developer can run by hand and CI can run automatically.

**Deliverables**
- [ ] `postman/ShopFlow.postman_collection.json` with one folder per API area: Auth, Products, Cart, Checkout, Orders, Webhooks, Admin.
- [ ] `postman/local.postman_environment.json`, with no hard-coded URLs or keys inside requests.
- [ ] At least **40 assertions** covering status codes, response bodies, JSON schema and response time.
- [ ] Positive and negative cases in every folder.
- [ ] Requests chained through variables, for example login → token → cart → checkout → order.
- [ ] A `postman/README.md` with the Newman command and how to read the report.

**Acceptance criteria**
- `newman run …` passes on a fresh database **and** passes again on a second run straight after, with no manual edits.
- Newman writes an HTML report to `reports/`.

---

## Task 7 — Integration testing

**Key outcome:** Proof that the UI, the API, the database and the notification outbox all agree with each other.

**Deliverables**
- [ ] `utils/db.py`: a **read-only** helper for querying `data/shopflow.db`.
- [ ] At least **6 integration tests**, marked `integration`. Each checks at least **3 layers**.
- [ ] `docs/INTEGRATION_TESTS.md` with a table: flow → layers checked → why this flow matters.

**Acceptance criteria**
- Each failure message names the layers that disagree and their values.
- All tests pass on `main`.

**Git practice:** `blame`, `show`

---

## Task 8 — Non-functional testing

**Key outcome:** Requirements that go beyond "does the feature work" are identified, tested and justified.

**Deliverables**
- [ ] `docs/NON_FUNCTIONAL.md` covering:
  - which requirements you treat as non-functional, quoting the user story;
  - which risk each one carries;
  - how you test it;
  - what you chose **not** to test and why.
- [ ] Tests for at least **2** non-functional requirements.

**Acceptance criteria**
- The tests give the same result across **20 repeated runs** on `main`.
- The PR explains how you made sure the tests are meaningful, not just green.

**Git practice:** `cherry-pick`

---

## Task 9 — Jenkins pipeline

**Key outcome:** The quality gate runs automatically and gives a clear pass/fail, with reports.

**Deliverables**
- [ ] Jenkins running locally, Docker is fine. Note the setup steps in the PR.
- [ ] A declarative `Jenkinsfile` in the repo with these stages:
  - checkout
  - start the app with Docker Compose and wait until it's healthy
  - install dependencies
  - smoke tests
  - API tests with Newman
  - full regression (full runs only)
  - publish reports
  - always stop the app at the end
- [ ] A parameter to choose `smoke` or `full`.
- [ ] A nightly scheduled `full` run.
- [ ] A Multibranch Pipeline job, so PR branches run the smoke stage.

**Acceptance criteria**
- The smoke run finishes in **under 10 minutes**.
- JUnit results and HTML reports are visible in Jenkins.
- Two runs in a row both succeed, because the environment is cleaned up each time.
- The PR includes screenshots of a **green** build and a deliberately **red** build.

**Git practice:** `revert`

---

## Task 10 — Optimization and reliability

**Key outcome:** A faster and more trustworthy suite, with the improvement proven by numbers.

**Deliverables**
- [ ] `docs/METRICS.md` with a before/after table covering:
  - total runtime;
  - the 10 slowest tests;
  - pass rate over 20 runs on `main`.
- [ ] Parallel execution with `pytest-xdist`.
- [ ] `docs/FLAKY_TESTS.md`: your written policy for detecting, investigating, retrying and quarantining unstable tests, and when a failure must **not** be treated as flaky.

**Acceptance criteria**
- The full suite is at least **30% faster** than your Task 3 baseline.
- The pass rate on `main` is at least 98% over 20 runs.
- Any test in quarantine has a linked JIRA ticket explaining why.

**Git practice:** squash your own local commits before pushing (`reset --soft`)

---

## Task 11 — Test management

**Key outcome:** Your automation is connected to the team's tools, with full traceability from requirement to result.

**Deliverables**
- [ ] **TestRail:**
  - a project with one section per user story;
  - at least **40 test cases**, each with preconditions, steps and expected result;
  - each case marked as automated (with the test name) or manual (with a reason).
- [ ] **TestRail integration:** each pipeline run creates a TestRail run and posts the results automatically.
- [ ] **`docs/TRACEABILITY.md`:** user story → TestRail case IDs → automated tests → latest result.
- [ ] **JIRA:**
  - a Scrum board with Tasks 1–12 as stories, planned into 1-week sprints;
  - a short retro note at the end of each sprint.
- [ ] **Confluence:** pages for framework architecture (with a diagram), how to run the tests, test strategy, and the defect triage process.

**Acceptance criteria**
- Every user story has at least one test case, and every test case traces to a story.
- Links to TestRail, JIRA and Confluence are in the PR description. Free tiers or trials are fine.

---

## Task 12 — Release v1.1 assessment

**Key outcome:** A justified, evidence-based GO / NO-GO decision for the next release.

`release/v1.1` is the next release candidate. You are the release quality gate.

**Deliverables**
- [ ] Your full suite, UI and API and Newman and integration and non-functional, run against `release/v1.1`. Attach the reports.
- [ ] Every defect you find logged in **JIRA**, following `.github/ISSUE_TEMPLATE/bug_report.md`. Each one includes:
  - steps to reproduce;
  - expected and actual results;
  - evidence;
  - severity;
  - frequency.
- [ ] A **root cause analysis** for every defect, covering:
  - the category (code, data, environment, or test);
  - the evidence;
  - the commit that introduced it;
  - how to prevent it in future.
- [ ] `docs/RELEASE_v1.1_REPORT.md` covering:
  - scope tested;
  - results per layer;
  - the defect list by severity;
  - risks;
  - a **GO / NO-GO** recommendation with reasons.
- [ ] A **20-minute walkthrough**: demo the pipeline, present two RCAs, and defend your decision.

**Acceptance criteria**
- Every defect is backed by evidence from a test, not from reading code.
- At least one root cause is located with `git bisect`, with the output in the RCA.
- The report is merged into `main` through a PR.

> Find problems by testing first. Then use Git history as your tool to confirm and locate the cause.

**Git practice:** `fetch`, `diff` between branches, `bisect`

---

## Final checklist

- [ ] Tasks 1–11 merged into `main` through reviewed pull requests
- [ ] Release report, JIRA defects and RCAs from Task 12
- [ ] Clean Git history: feature branches, meaningful commits, `v1.0.0` tag
