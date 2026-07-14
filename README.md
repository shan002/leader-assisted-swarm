# leader-assisted-swarm

This repository contains a simulation with two initially separated milling swarms and one human-controlled leader.

The agents follow the same binary sensing rule:

- If another agent is detected, perform action `a`.
- If nothing is detected, perform action `b`.

The leader is controlled manually and is treated like any other detectable agent.

The objective is to use the leader to:

1. Bring the two milling groups together.
2. Move the combined milling group toward the end point.
3. Escape from the combined group without breaking the milling structure.

## Questions

**Question 1:** Does the same approach still work when each group contains more than three agents (`n > 3`)?

**Question 2:** After the two milling groups merge, can the leader escape from the combined milling structure?

## Display

The simulation shows:

- A red center marker for Group A
- A blue center marker for Group B
- One yellow center marker after the groups merge
- A white marker for the final end point
- Whether the groups are separate or merged
- The current loss
- The minimum loss reached during the run
- The distance from the combined group center to the end point
- The circliness score

Before the two groups merge, the simulation shows two separate center markers.

After the groups merge, the two markers are replaced by one combined center marker.

The loss is calculated only after the two groups merge.

## Loss Function

The loss is calculated as:

$$
J = d_{\text{goal}} + (1 - C)
$$

where:

- \(d_{\text{goal}}\) is the distance between the center of the combined group and the end point.
- \(C\) is the circliness score of the combined group.
- \(1-C\) is the milling loss.

A lower loss is better.

The best possible loss is `0`. This means:

- The center of the combined group is exactly at the end point.
- The circliness score is `1`.

The simulation displays both the current loss and the minimum loss reached during the run.

## Quickstart

```bash
git clone https://github.com/shan002/leader-assisted-swarm
cd leader-assisted-swarm

uv venv
source .venv/bin/activate

uv pip install -r requirements.txt
python run_simulation.py