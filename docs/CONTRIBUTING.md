# Git workflow (follow this for every task)

Step-by-step version, including what to click on GitHub: **[GITHUB_GUIDE.md](GITHUB_GUIDE.md)**.

```bash
git clone <repo-url> && cd automationtesting
git checkout main && git pull                 # always start from fresh main
git checkout -b feature/<issue-number>-<short-name>

# ...work, then review what you changed...
git status
git diff
git add <files>                               # stage intentionally, not blindly
git commit -m "Add checkout page object and data-driven pricing tests"

git push -u origin feature/<issue-number>-<short-name>
# open a Pull Request into main, link the issue ("Closes #N"), request review
```

Good habits: small commits · meaningful messages · one task per branch · never commit secrets or `.db` files ·
`git pull --rebase` before pushing if `main` moved · resolve conflicts locally and re-run tests before pushing.

## Commands you will practise in this project
`clone` · `branch` · `checkout/switch` · `add` · `commit` · `push` · `pull` · `fetch` · `merge` · `rebase` ·
`stash` · `log --oneline --graph` · `diff` · `blame` · `restore` · `revert` · `tag` · **`bisect`** (to find the commit that broke something)

## Suggested layout for your work
```
tests/            # pytest suites (ui/, api/, integration/)
pages/            # page objects
data/             # test data files
postman/          # collection + environments
Jenkinsfile
conftest.py
pytest.ini
```
