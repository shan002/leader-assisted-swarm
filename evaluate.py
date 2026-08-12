"""Evaluate the leader controller over multiple headless runs."""

import argparse
import random

import numpy as np

from run_simulation import build_world


def evaluate(runs, first_seed):
    scores = []
    catches = 0

    for run in range(runs):
        seed = first_seed + run
        random.seed(seed)
        np.random.seed(seed)
        world, score = build_world(seed)
        world.setup()
        while not score.finalized:
            world.step()

        scores.append(score.final_score)
        catches += score.outcome == "CAUGHT"
        print(f"Run {run + 1:>2}/{runs}: seed={seed}, {score.outcome}, score={score.final_score:.4f}")

    print()
    print(f"Runs: {runs}")
    print(f"Caught: {catches}")
    print(f"Catch rate: {100.0 * catches / runs:.2f}%")
    print(f"Average score: {np.mean(scores):.4f}")


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate the leader controller without a GUI.")
    parser.add_argument("runs", nargs="?", type=int, default=10, help="number of runs (default: 10)")
    parser.add_argument("--seed", type=int, default=1, help="base seed (default: 1)")
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("runs must be at least 1")
    return args


if __name__ == "__main__":
    args = parse_args()
    evaluate(args.runs, args.seed)
