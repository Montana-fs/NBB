# MVP Bootstrap

A pre-configured empty project folder for starting a new MVP with the `mvp-builder` Claude Code skill.

## What's in here

```
.
├── CLAUDE.md                              # Starter project memory (skill will replace)
├── README.md                              # This file
└── .claude/
    ├── settings.local.json                # Auto-approved permissions for known-good tools
    └── skills/
        └── mvp-builder/                   # The bundled skill (auto-discovered)
            ├── SKILL.md
            ├── assets/
            └── docs/
```

## Usage

1. **Unzip** this archive into an empty folder where you want your new project to live:

   ```bash
   unzip mvp-bootstrap.zip -d my-new-project
   cd my-new-project
   ```

2. **Open Claude Code** in that folder:

   ```bash
   claude
   ```

3. **Tell Claude what you want to build** — in plain English or Danish. Examples:
   - *"I want to build a CRM to track my customers and orders"*
   - *"jeg vil gerne bygge et system til at holde styr på mine kunder"*
   - *"/mvp-builder"* (to invoke it manually)

The `mvp-builder` skill auto-activates, walks you through an interview, and builds the app step by step. You do not need to know any code.

## What auto-approved permissions mean

The `.claude/settings.local.json` pre-approves common safe commands (`npm`, `git`, `node`, `ls`, `mkdir`, etc.) so Claude doesn't stop and ask every few seconds. Dangerous operations (`sudo`, `rm -rf *`, piping curl into a shell) stay blocked. Edit the file to adjust.

## Updating the skill

The skill is a copy in `.claude/skills/mvp-builder/`. To update:

1. Replace the folder with a newer version from your source repo.
2. Restart Claude Code (or edit files inline — live reload picks up changes).

## Requirements

- **Claude Code CLI** installed (`npm install -g @anthropic-ai/claude-code`)
- **Node.js 22+** and **Git** (the skill will detect and guide installation if missing)
- Windows 10/11 with PowerShell **or** Linux (Ubuntu, Debian, Fedora, Arch, openSUSE)
