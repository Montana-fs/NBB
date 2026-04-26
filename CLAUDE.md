# Project Memory

> This is a fresh project bootstrap. The `mvp-builder` skill will replace this file
> with a real project memory file once the idea has been captured and the project
> structure exists.

## About the user

- Non-developer. Explain in plain language, never assume technical knowledge.
- Primary language: [to be determined — Dansk / English / Mix]
- Onboarding style: [to be determined — Quick choices / Conversation / You decide for me]
- Operating system: [to be detected — Windows / Linux / macOS]

## How to start

Ask the user: *"What would you like to build?"* — or, if they just opened the project fresh, simply wait for them to describe their idea.

The `mvp-builder` skill activates automatically when the user:

- Describes a new app idea (EN: "I want to build…" / DA: "jeg vil gerne bygge…")
- Asks to continue ("let's continue" / "fortsæt projektet")
- Invokes it directly with `/mvp-builder`

## Where everything lives

- `.claude/skills/mvp-builder/` — the installed skill (do not edit; update via git from the source repo)
- Everything else in this folder will be created by the skill during bootstrap

## After bootstrap

The skill will replace this `CLAUDE.md` with a filled-in project memory file, and create:

- `docs/VISION.md` — the original "why" and interview answers (append-only)
- `docs/DECISIONS.md` — log of non-obvious choices (append-only)
- `docs/INSTALL.md` — how to install on a new machine
- `docs/SERVER.md` — how to run and operate the app
- `frontend/` + `backend/` — the actual app code

Read `docs/VISION.md` and `docs/DECISIONS.md` first on every future session.
