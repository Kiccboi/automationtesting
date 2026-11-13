# GitHub Guide for This Project

This guide shows exactly what to do in Git and GitHub, step by step. Follow **Part 1** once.
Then repeat **Part 2** for every task.

Commands go in a terminal:

- **Windows:** "Git Bash", installed with Git
- **macOS:** Terminal

Text in `<angle brackets>` is a placeholder. Replace it, including the brackets.

---

## Part 1 — One-time setup

### 1.1 Create a GitHub account and accept the invite
1. If you don't have one yet, sign up at https://github.com.
2. Send your GitHub username to the project owner.
3. You will get an email titled **"invited you to collaborate"**. Click **View invitation**, then **Accept invitation**.
4. Open https://github.com/Kiccboi/automationtesting. You should now see the code.

### 1.2 Install Git
- **Windows:** download from https://git-scm.com/download/win. Accept the defaults when installing. This also installs **Git Bash** and **Git Credential Manager**, which handles logging in for you.
- **macOS:** run `git --version` in Terminal and accept the prompt to install the developer tools.

Check that it worked:
```bash
git --version
```

### 1.3 Tell Git who you are (once per computer)
```bash
git config --global user.name  "Aarthi Kanuganti"
git config --global user.email "<the email on your GitHub account>"
git config --global init.defaultBranch main
```

### 1.4 Get the project onto your computer (clone)
1. On the repo page, click the green **Code** button → **HTTPS** → copy the URL.
2. In the terminal, go to the folder where you keep projects, then run:
   ```bash
   cd ~/Documents
   git clone https://github.com/Kiccboi/automationtesting.git
   cd automationtesting
   ```
3. The first time Git talks to GitHub, a browser window opens. Sign in to GitHub and click **Authorize**. This only happens once.

### 1.5 Look around
```bash
git status                          # what branch you're on, any changes
git branch -a                       # all branches, including the ones on GitHub
git log --oneline --graph --all     # the history as a graph
```

You will see `main` and `remotes/origin/release/v1.1`.
`origin` is Git's name for the GitHub copy of the repo.

### 1.6 Create the `v1.0.0` tag (part of Task 0)
```bash
git checkout main
git tag -a v1.0.0 -m "ShopFlow v1.0.0 baseline"
git push origin v1.0.0
```

Check it on GitHub: the repo page should now show **1 Tags**.

### 1.7 Tour of the GitHub website
| Tab | What it's for in this project |
|---|---|
| **Code** | Browse files. Use the branch dropdown (top left) to switch between `main` and other branches. |
| **Issues** | Your 12 tasks. Each issue is one task. |
| **Pull requests** | Where you submit each finished task for review. |
| **Commits** (clock icon on the Code tab) | The history of every change. |

---

## Part 2 — The routine for every task

Example: you are starting **Task 2 — Page objects**, which is issue **#2**.

### 2.1 Start from the latest `main`
```bash
git checkout main
git pull
```
Always do this before starting a new task, so you build on everything already merged.

### 2.2 Create your task branch
```bash
git checkout -b feature/2-page-objects
```
The pattern is `feature/<issue-number>-<short-name>`, using lowercase and hyphens.
Check where you are with `git branch`. The current branch has a `*` next to it.

### 2.3 Work and commit in small steps
After each meaningful piece of work, for example "added LoginPage":
```bash
git status                     # see what changed
git diff                       # see exactly what changed, line by line
git add pages/login_page.py    # stage the files you want in this commit
git status                     # check what is staged (green) vs not (red)
git commit -m "Add LoginPage page object"
```

**Good commit messages** start with a verb and say what changed:

| Good | Bad |
|---|---|
| `Add LoginPage page object` | `changes` |
| `Fix flaky wait in CartPage` | `fix` |
| `Move base URL into config` | `update files` |

**Never commit** `.venv/`, `*.db`, `reports/`, passwords or keys. They are already listed in `.gitignore`.
If `git status` shows one of them, don't `git add` it.

### 2.4 Push your branch to GitHub
The first push of a new branch:
```bash
git push -u origin feature/2-page-objects
```
After that, just:
```bash
git push
```
Push at least once at the end of each working day, so your work is backed up.

### 2.5 Open a pull request (PR)
1. Go to the repo on GitHub. A yellow bar says **"feature/2-page-objects had recent pushes"**. Click **Compare & pull request**.
   (If you don't see the bar, go to **Pull requests** → **New pull request**. Set **base: main** and **compare: feature/2-page-objects**.)
2. Check that the arrow reads **base: `main` ← compare: `feature/2-page-objects`**.
3. **Title:** for example `Task 2: Page objects`.
4. **Description:** the template is filled in for you. Complete it:
   - Write `Closes #2` on its own line. GitHub then closes issue #2 automatically when the PR is merged.
   - Say what you did and how you tested it, for example "ran `pytest -m smoke`, 12 passed".
   - Attach screenshots where the task asks for them. You can drag and drop images into the box.
5. Click **Create pull request**.
6. Tell the project owner the PR number, for example "PR #14 is ready".

**Don't merge your own PR.** The owner reviews it and merges it.

### 2.6 Respond to review comments
The review appears on the PR's **Conversation** and **Files changed** tabs.

1. Make the requested changes on the **same branch**:
   ```bash
   git checkout feature/2-page-objects
   # edit files...
   git add <files>
   git commit -m "Address review: move waits into BasePage"
   git push
   ```
2. The PR updates automatically. You don't need to open a new one.
3. Reply to each comment, for example "Done in <commit>" or a short explanation if you disagree. Then click **Resolve conversation**.
4. Tell the owner it's ready for another look.

### 2.7 After your PR is merged
```bash
git checkout main
git pull                                   # get the merged work
git branch -d feature/2-page-objects       # delete your local copy of the branch
```
On GitHub, click **Delete branch** on the merged PR page.

Then go back to **2.1** for the next task.

---

## Part 3 — Things that will come up

### "main moved while I was working" (keep your branch up to date)
```bash
git checkout main
git pull
git checkout feature/4-pricing-tests
git rebase main          # replay your commits on top of the latest main
git push --force-with-lease
```
Only force-push **your own feature branch**, never `main`.

### Merge conflicts
Git stops and lists the conflicting files. Open each file and find the markers:
```
<<<<<<< HEAD
the version from main
=======
your version
>>>>>>> your commit
```
1. Edit the file so it contains the correct final code, and delete the marker lines.
2. Run your tests.
3. Then:
   ```bash
   git add <file>
   git rebase --continue     # or: git commit   (if you were merging)
   ```
4. To give up and go back to how things were: `git rebase --abort` or `git merge --abort`.

### Switch tasks without committing half-done work
```bash
git stash            # put your changes aside
git checkout main    # do something else...
git checkout feature/4-pricing-tests
git stash pop        # bring the changes back
```

### Undo things safely
| Situation | Command |
|---|---|
| Throw away uncommitted changes to a file | `git restore <file>` |
| Unstage a file you added by mistake | `git restore --staged <file>` |
| Fix the message of your last commit (before pushing) | `git commit --amend -m "Better message"` |
| Undo your last commit but keep the changes (before pushing) | `git reset --soft HEAD~1` |
| Undo a commit that is already pushed | `git revert <commit-sha>` |

### Look at history
```bash
git log --oneline --graph --all
git show <commit-sha>                 # what one commit changed
git log -p <file>                     # every change to one file
git blame <file>                      # who last changed each line
git diff main..origin/release/v1.1    # compare two branches
```

### Try out the release candidate (Task 12)
```bash
git fetch origin
git checkout -b qa/release-v1.1-assessment origin/release/v1.1
```

### Find which commit broke something (`git bisect`)
Use this when something works on one commit and fails on a later one. Git does a binary search through the commits between them:
```bash
git bisect start <bad-commit> <good-commit>
# Git checks out a commit in the middle. Test it, then tell Git the result:
git bisect good      # or: git bisect bad
# repeat until Git prints "<sha> is the first bad commit"
git bisect reset     # go back to where you started
```
If a single test command can decide good or bad, Git can run it for you:
`git bisect run <command>`

---

## Part 4 — Common errors

| Error | What it means / what to do |
|---|---|
| `Permission denied` / `403` when pushing | You haven't accepted the collaborator invite, or you signed in with a different account. Accept the invite and try again. |
| `rejected ... (fetch first)` / `non-fast-forward` | GitHub has commits you don't have. Run `git pull --rebase`, then push again. |
| `Your local changes would be overwritten` | Commit or `git stash` your changes before switching branches or pulling. |
| `fatal: not a git repository` | You're in the wrong folder. `cd` into `automationtesting`. |
| You committed on `main` by mistake (not pushed yet) | `git branch feature/<n>-<name>`, then `git reset --hard origin/main`, then `git checkout feature/<n>-<name>`. Your commits are now on the new branch. |
| `CONFLICT` during pull/rebase/merge | See **Merge conflicts** above. |

When stuck, run `git status` first. It usually tells you what to do next.
