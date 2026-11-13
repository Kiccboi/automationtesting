# ShopFlow QA Challenge: Task Guide

This guide tells you **what** to deliver for each task and the standard it must meet.
**How** you design and write the tests is up to you. That is what's being assessed.

Each task matches a GitHub issue with the same number. Plan for about **4 weeks part-time**.

## Rules for the whole project

- One task = one branch = one pull request. Never commit straight to `main`.
- Name branches `feature/<issue-number>-<short-name>`. The PR description says `Closes #<issue-number>` and explains how you tested your work.
- Build everything against `main`. Use `release/v1.1` only in Task 12.
- Never commit `.db` files, virtual environments, generated reports or secrets.
- The requirements are in `docs/USER_STORIES.md`. If something is unclear, write down your assumption and raise it in review, as you would on a real team.

---

## Task 0 — Setup (no issue)

- Install what you need, clone the repo, and run the app locally. Instructions are in the README.
- Use the app by hand until you understand every feature in the user stories.
- Create and push an annotated tag `v1.0.0` on the current `main` commit.
- Bring a list of questions or assumptions about the requirements to your first review.

**Done when:** the app runs locally, and tag `v1.0.0` is visible on GitHub.

---

## Task 1 — Framework skeleton

Set up a Python + Pytest + Selenium project that every later task can build on.

**Acceptance criteria**
- A clear folder structure for tests, page objects, utilities, test data and configuration.
- Settings (URL, browser, headless mode, timeouts and so on) can be changed without editing code.
- Markers at least for `smoke`, `regression`, `integration` and `api`.
- Every run produces an HTML report, and a failing UI test attaches a screenshot.
- At least one passing smoke test.

**Git practice:** `checkout -b`, `add`, `commit`, `push -u`, opening a pull request

---

## Task 2 — Page objects

Model the storefront using the Page Object Model.

**Acceptance criteria**
- Every page in the app has a page object.
- Locators and waits live only in page objects, never in tests.
- No hard-coded sleeps anywhere in the framework.
- UI tests covering US-1, US-2 and US-3, all passing on `main`.

**Git practice:** small focused commits, reviewing your own diff before committing, responding to review comments

---

## Task 3 — API client and test data

Make test setup fast and independent of the UI.

**Acceptance criteria**
- A reusable API client for the ShopFlow REST API.
- Fixtures that create the data a test needs (users, products and so on) through the API.
- Tests can run in any order and on their own.
- The PR states the suite runtime before and after this task.

**Git practice:** `stash`, `pull --rebase`

---

## Task 4 — Data-driven pricing tests

Verify the pricing and checkout rules in US-4.

**Acceptance criteria**
- Test cases live in an external data file. Adding a case means adding data, not code.
- At least 25 cases. You choose them using test-design techniques, and the PR names which techniques you used.
- Expected values come from the requirements, not from the app's own output.
- Pricing is verified both through the API and through the UI.

**Git practice:** resolve at least one merge conflict

---

## Task 5 — Order lifecycle

Verify the order and payment behaviour described in the user stories.

**Acceptance criteria**
- The PR includes your own diagram of the order lifecycle, drawn from the requirements.
- Valid and invalid transitions are both covered.
- Asynchronous behaviour is handled without fixed sleeps.

**Git practice:** `commit --amend`, `log`

---

## Task 6 — Postman collection

Build an API test collection that a developer can run by hand and CI can run automatically.

**Acceptance criteria**
- A Postman collection and environment committed to the repo.
- It covers positive and negative scenarios for the API, with assertions on status, response body and schema.
- It runs from the command line with Newman and produces a report.
- It can be run repeatedly against the same environment without manual edits.

---

## Task 7 — Integration testing

Verify that the parts of the system agree with each other. The parts are the UI, the API, the database and the notification outbox.

**Acceptance criteria**
- Integration tests that each check more than one layer.
- When a test fails, its message makes clear which layer disagreed.
- The PR explains which flows you chose to cover and why.

**Git practice:** `blame`, `show`

---

## Task 8 — Non-functional testing

Decide which requirements need non-functional testing, such as concurrency, reliability or performance, and test them.

**Acceptance criteria**
- The PR explains which requirements you treated as non-functional, and your approach.
- The tests give consistent results across repeated runs on `main`.

**Git practice:** `cherry-pick`

---

## Task 9 — Jenkins pipeline

Run the quality gate automatically.

**Acceptance criteria**
- A `Jenkinsfile` committed to the repo.
- The app is started and stopped by the pipeline, using Docker Compose.
- A quick smoke run for pull requests (under 10 minutes), and a scheduled full regression run.
- Test results and reports are published in Jenkins.
- The PR includes screenshots of a passing build and a failing build.

**Git practice:** `revert`

---

## Task 10 — Optimization and reliability

Make the suite faster and more trustworthy, and prove it with numbers.

**Acceptance criteria**
- Before and after metrics: total runtime, slowest tests and pass-rate stability.
- Parallel execution.
- A written policy, `docs/FLAKY_TESTS.md`, on how you handle unstable tests.

**Git practice:** squash your own local commits before pushing

---

## Task 11 — Test management

Connect the automation to the team's tools.

**Acceptance criteria**
- **TestRail:** test cases for every user story, each linked to its automated test where one exists. Results are published per run.
- **Traceability:** user story → test case → automated test → latest result.
- **JIRA:** a Scrum board with these tasks planned into sprints, plus a short retro note per sprint.
- **Confluence:** pages on framework design, how to run the tests, and your test strategy.

The free tiers or trials of these tools are fine.

---

## Task 12 — Release v1.1 assessment

`release/v1.1` is the next release candidate. Act as the release quality gate.

**Acceptance criteria**
- Your full suite has been run against `release/v1.1`.
- Every defect you find is logged in JIRA, using `.github/ISSUE_TEMPLATE/bug_report.md`, with evidence.
- Every defect has a root cause analysis: category, evidence, the change that introduced it, and how to prevent it in future.
- `docs/RELEASE_v1.1_REPORT.md` contains the scope, results, defects, risks and a **GO / NO-GO** recommendation with reasons.
- A 20-minute walkthrough of your work and your decision.

> Find problems by testing first. Then use Git history as your tool to confirm and locate the cause.

**Git practice:** `fetch`, `diff` between branches, `bisect`

---

## Final checklist

- [ ] Tasks 1–11 merged into `main` through reviewed pull requests
- [ ] Release report and RCAs from Task 12
- [ ] Clean Git history and a `v1.0.0` tag
