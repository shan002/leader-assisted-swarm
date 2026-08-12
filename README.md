# leader-assisted evader capture

This is a programming challenge. A blue evader starts at a random
point on the far-right side and moves in a straight line toward the red
protected point on the left. The green leader must guide the milling swarm so
that a defender touches the evader
before it reaches the protected point.

The defenders keep their existing binary sensing rule:

- If an agent is detected, perform action `a`.
- If nothing is detected, perform action `b`.

## Task

Edit only `leader_controller.py`. Do not rename the file or the
`LeaderController` class.

The controller must return the leader's forward and turning speeds:

```python
def get_actions(self, agent):
    return linear_velocity, angular_velocity
```

The evader can be found with:

```python
evader = next(other for other in agent.world.population if other.team == "evader")
```

The leader must influence the defenders only by moving. Do not directly change
an agent's position, heading, sensor, controller, or the scoring values.

## Run

```bash
git clone --branch beeline-evader-detection --single-branch https://github.com/shan002/leader-assisted-swarm.git
cd leader-assisted-swarm

uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
python run_simulation.py
```

Use the activation command for your shell:

| Shell | OS | Activation command |
|---|---|---|
| CMD.exe | Windows | `.\.venv\Scripts\activate` |
| PowerShell | Windows | `.\.venv\Scripts\activate.ps1` |
| NuShell | Windows | `overlay use .\.venv\Scripts\activate.nu` |
| bash/zsh | Linux/macOS | `source .venv/bin/activate` |
| Fish | Linux/macOS | `source .venv/bin/activate.fish` |
| NuShell | Linux/macOS | `overlay use .venv/bin/activate.nu` |

To start paused:

```bash
python run_simulation.py --start_paused
```

Controls:

- Space: pause or continue.
- R: start a new run after the result is shown.
- Q: quit.

Each run uses a different seed. The current seed is shown on the screen and in
the terminal output.

To reproduce a run with a specific starting seed:

```bash
python run_simulation.py --seed 42
```

To evaluate the controller over 10 runs without opening the GUI:

```bash
python evaluate.py
```

Pass a different number of runs if needed:

```bash
python evaluate.py 20
```

Evaluation uses base seed `1` by default. Keep this unchanged to compare your score with others. 

To use another base seed:

```bash
python evaluate.py 20 --seed 42
```

## Score

If a defender touches the evader:

```text
score = capture time + (1 - circliness)
```

If the evader reaches the protected point without being caught:

```text
score = evader arrival time + 2
```

Lower is better. A successful capture always scores better than a miss. The
simulation ends automatically on capture or when the evader reaches the
protected point.

## Submit

Post your result after running `evaluation.py` and attach `leader_controller.py`:

```text
Runs:
Caught:
Catch rate:
Average score:
```

The result will be checked using the unchanged `world.yaml` with the base seed `1` of `evaluation.py`.
