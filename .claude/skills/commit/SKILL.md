---
name: commit
description: Automate the git commit workflow — lint, format, stage, and commit with a well-crafted message. Only use when the user explicitly invokes /commit — never trigger proactively or as part of another task.
---

# Commit

A rigid, step-by-step workflow for committing changes. Follow these steps exactly in order — no skipping, no reordering.

## Step 1: Gather context (parallel)

Run all three in parallel in a single turn:

```
git status
git diff
git log --oneline -5
```

If there are no changes (nothing to commit), tell the user and stop.

## Step 2: Lint and format

Run ruff to fix and format the codebase:

```
uv run ruff check --fix . && uv run ruff format .
```

If ruff reports unfixable errors, stop and fix them before proceeding. Never commit code that fails ruff.

If ruff changed any files, run `git diff --stat` to see what ruff modified — these changes get included in the commit too.

## Step 3: Stage files

Stage the relevant changed files by name. Be selective:

- **DO** stage: source code, config, tests, migrations, CLAUDE.md, pyproject.toml, uv.lock
- **NEVER** stage: `.env`, credentials, secrets, `db.sqlite3`, `__pycache__/`, `.pyc` files

Use `git add <file1> <file2> ...` with explicit file names — avoid `git add .` or `git add -A`.

## Step 4: Draft commit message

Analyze the staged changes and write a commit message:

- One concise summary line (imperative mood, under 72 chars)
- Focus on the **why**, not the what
- "add" = new feature, "update" = enhancement, "fix" = bug fix
- If the change is simple enough, one line is sufficient
- For larger changes, add a blank line then a short body with relevant details

## Step 5: Create the commit

Use a HEREDOC to pass the message, always ending with the Co-Authored-By trailer:

```bash
git commit -m "$(cat <<'EOF'
<summary line>

<optional body>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Step 6: Verify

Run `git status` to confirm the commit succeeded and the working tree is clean (or shows only intentionally unstaged files).

Report the commit hash and summary to the user.
