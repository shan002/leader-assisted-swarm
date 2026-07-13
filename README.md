# leader-assisted-swarm

This repository contains a simulation with two initially separated milling swarms and one human-controlled leader.

The agents follow the same binary sensing rule:

* If another agent is detected, perform action `a`.
* If nothing is detected, perform action `b`.

The leader is controlled manually and is treated like any other detectable agent. The objective is to use the leader to bring the two milling groups together.

**Question:** Does the same approach still work when each group contains more than three agents (`n > 3`)?

## Quickstart

```bash
git clone https://github.com/shan002/leader-assisted-swarm
cd leader-assisted-swarm

uv venv
source .venv/bin/activate

uv pip install -r requirements.txt
python run_simulation.py
```

Depending on your operating system and shell, use the appropriate environment activation command:

| Shell      | OS          | Activation command                        |
| ---------- | ----------- | ----------------------------------------- |
| CMD.exe    | Windows     | `.\.venv\Scripts\activate`                |
| PowerShell | Windows     | `.\.venv\Scripts\activate.ps1`            |
| NuShell    | Windows     | `overlay use .\.venv\Scripts\activate.nu` |
| bash/zsh   | Linux/macOS | `source .venv/bin/activate`               |
| Fish       | Linux/macOS | `source .venv/bin/activate.fish`          |
| NuShell    | Linux/macOS | `overlay use .venv/bin/activate.nu`       |
