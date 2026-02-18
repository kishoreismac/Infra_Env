# Infra_Env

Infrastructure environment session tracker - A simple tool to track and display recent infrastructure session activity.

## Features

- Track sessions with timestamp, environment, user, and description
- List recent sessions
- Persistent storage of session history
- Command-line interface

## Installation

No external dependencies required - uses only Python 3 standard library.

## Usage

### List Recent Sessions

```bash
python sessions.py list
```

List a specific number of recent sessions:

```bash
python sessions.py list -n 20
```

### Add a New Session

```bash
python sessions.py add production john.doe
```

Add a session with description:

```bash
python sessions.py add staging jane.smith -d "Deployment testing"
```

### Clear All Sessions

```bash
python sessions.py clear
```

## Examples

```bash
# Add some sessions
python sessions.py add production alice -d "Database migration"
python sessions.py add staging bob -d "Feature testing"
python sessions.py add development charlie

# List recent sessions
python sessions.py list

# Output:
# Recent Sessions:
# --------------------------------------------------------------------------------
# 2026-02-18 08:50:00 | development     | charlie         |
# 2026-02-18 08:49:30 | staging         | bob             | Feature testing
# 2026-02-18 08:49:00 | production      | alice           | Database migration
```

## Data Storage

Sessions are stored in `~/.infra_env_sessions.json` (in the user's home directory). The tool automatically maintains the last 50 sessions.