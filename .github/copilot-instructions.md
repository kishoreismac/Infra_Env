# Copilot Instructions for Infra_Env

## Repository Overview

**Infra_Env** is a repository for managing infrastructure environments. It is currently in early setup and is being onboarded to GitHub Copilot coding agent workflows.

## Repository Structure

```
.
├── README.md                  # Project overview
├── agents/
│   └── ecognity.agent.md      # Custom Copilot agent definition template
└── .github/
    └── copilot-instructions.md  # This file
```

## Key Conventions and Practices

### Language and Runtime
- This repository is expected to use **Python** for any scripting or tooling code.
- Use the standard library where possible before adding third-party dependencies.

### Testing
- Use the **`unittest`** framework for writing tests.
- Use **`tempfile.NamedTemporaryFile`** when tests require file-based or persistence-related fixtures.
- Test files are named `test_<module>.py` and co-located or placed in a `tests/` directory.

### Session Tracking (planned feature)
- Sessions are stored in JSON format at `~/.infra_env_sessions.json`.
- The session list is capped at **50 entries** to prevent unbounded growth.
- See `sessions.py` (to be added) for the implementation and `test_sessions.py` for tests.

### Custom Agents
- Agent definitions live under the `agents/` directory using `.agent.md` files.
- Follow the format in `agents/ecognity.agent.md` when adding new agent definitions.
- The `name` and `description` front-matter fields are required.
- Merge agent files into the default branch to make them available.

## How to Work in This Repository

1. **Explore first**: The repository is minimal. Check `README.md` and `agents/` before making changes.
2. **Python code**: Place Python modules at the repository root or in a `src/` subdirectory; keep tests in `tests/` or alongside the module they test.
3. **Running tests**: Use `python -m unittest discover` from the repository root to discover and run all tests.
4. **No build step required**: There is no compilation step; Python files can be run directly.
5. **Adding dependencies**: If a `requirements.txt` does not yet exist, create one. Prefer pinned versions for reproducibility.

## Known Issues / Errors Encountered

- No errors have been encountered yet. This file will be updated as the repository evolves.

## CI / Workflow

- No CI workflows have been configured yet. When adding GitHub Actions, place workflow files under `.github/workflows/`.
- Recommended first workflow: a simple `python -m unittest discover` run on push/pull_request events.
