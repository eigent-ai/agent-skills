---
name: env-hub
description: Save a finished Claude Code or Codex session as a Harbor task (an agent benchmark task) and submit it to Env Hub, which turns it into an environment by writing its verifier and reference solution. Use when the user asks to "save this session as a Harbor task", "turn this into a Harbor task or environment", "submit this to Env Hub", "保存为 Harbor 任务", or to check how a submitted task is going or list their environments.
---

# Env Hub

`scripts/capture.py` (in this skill's folder; Python 3.9+, standard library
only) does every step. Run it with the absolute path to this skill's folder.

## Save

First read the user's messages in the session, numbered:

```bash
python3 <skill>/scripts/capture.py messages --from claude --json   # or: --from codex
```

It reads the newest session that ran in the current folder (`--session ID` or
`--transcript FILE` for another; `sessions --from claude` lists them).

Choose the messages that state the task: the request, and later messages that
correct it or add to it. Leave out what is not the task: asking to save or
submit, thanks, questions about this skill, and a different task in the same
session (save that one on its own). `taken_by_default` marks what `save` takes
without a choice: every message before the request to save. Then:

```bash
python3 <skill>/scripts/capture.py save --from claude --session ID --messages 1,3 --json
```

`--messages` takes numbers and ranges (`1,3`, `2-4`). The instruction is the
chosen messages word for word: choose, never rewrite. The conversation kept
runs from the first chosen message through your replies to the last. A task
that starts at a later message starts from the last commit before it, so
earlier work in the session is there only if it was committed; say so when it
matters. The folder must be a git repository. Nothing leaves the machine and
the repository is not changed.

Beside the task folder it keeps the conversation (what the user and the agent
said, without the tools' output, anything that looks like a secret redacted)
and a bundle of both, the zip Env Hub takes.

Show the user the summary: the instruction, which of their messages were taken
and which left out and why (`messages`, `messages_left_out`), how many files
the workspace keeps, what was left out and why (`files_omitted`), every file
left out because it looks like a secret (`secrets_left_out`), and that the
conversation goes with the task (`conversation_turns`). To leave out files,
run `save` again with `--exclude PATH` (repeatable); to change what the task
says, again with other `--messages`.

- Never edit the saved task's files.
- If `save` says the chosen messages hold what looks like a secret, stop and
  tell the user; do not work around it.

## Submit (only after the user says yes)

Submitting uploads the bundle (the task and the conversation) to Env Hub under
the user's Eigent account, as the contribution agreement they accept says, and
starts converting it into an environment. Ask first, every time; say what will
be uploaded (the bundle and its size). Then:

```bash
python3 <skill>/scripts/capture.py submit <task folder> --json
```

The first time, the user signs in: run `capture.py login`, which opens their
browser (Eigent account, Google or GitHub) and asks them to accept the
contribution agreement and allow the skill. Never handle their password or
token; the script keeps the token in `~/.config/env-hub/`.

## Follow it

```bash
python3 <skill>/scripts/capture.py status <conversion id> --json
python3 <skill>/scripts/capture.py list --json     # the user's environments
```

`status`: `queued`, `running`, `succeeded` (`environment_url` is where the user
sees the environment in full, verifier and solution included) or `failed`
(`error.message` says why). Until then the user follows it on the web at
`account_url`, which `submit` and `status` return; give that address, never
one of your own (the hub may not be the default one). `stage` says more: `checking`, `publishing`,
`drafting` (Env Hub writes the verifier and reference solution), `gating`
(oracle and nop runs), `repairing`, `passed`, `rejected`, `needs_attention`.
Drafting and gating take minutes; check back rather than waiting in a loop.

Errors you can act on: "not signed in", an expired connection or an agreement
to accept → `login`; the day's limit → try later; the task too large → `save`
again with `--exclude` for large folders. The user removes Env Hub's access
from their account page on the hub.
