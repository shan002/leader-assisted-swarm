# leader-assisted-swarm

This is a programming challenge. The green leader must move a milling
swarm from the cyan start point to the red target.

The swarm agents have the same simple sensor used in our binary milling:

- If an agent is detected, they perform action `a`.
- If nothing is detected, they perform action `b`.

The swarm agents should not be changed. You should control only the leader.

## Task

Edit only `leader_controller.py`. Do not rename the file or the
`LeaderController` class.

The controller must return the leader's forward speed and turning speed:

```python
def get_actions(self, agent):
    return linear_velocity, angular_velocity
```

The controller can read the leader, swarm, and target information through
`agent`:

```python
agent.pos
agent.angle
agent.world.population
agent.world.meta["target"]
```

The defenders can be selected with:

```python
defenders = [other for other in agent.world.population if other.team == "defender"]
```

The leader must influence the swarm only by moving. Do not directly change an
agent's position, heading, sensor, controller, or the scoring values.

## Run

```bash
uv venv
source .venv/bin/activate
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

To open the simulation paused:

```bash
python run_simulation.py --start_paused
```

Controls:

- Space: pause or continue.
- Enter: finalize the current score.
- Q: close the simulation after finalizing.

The simulation also finalizes automatically when the score reaches the
`stop_score` in `world.yaml`.

## Score

```text
score = distance from swarm center to target + (1 - circliness)
```

Circliness is close to `1` when the agents form a circular mill and move around
its center. A lower score is better. The leader is not included in the score.

The display shows the current score and the lowest score reached during the
run. The final score is recorded when Enter is pressed or when `stop_score` is
reached. Time is measured in simulation time, so results are the same on
different computers.

## Submit

Post:

```text
Time:
Score:
Final step:
```

Also attach `leader_controller.py`. The result will be checked by running that file
with the unchanged `world.yaml`.
