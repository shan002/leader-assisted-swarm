"""Official scoring and completion logic for the leader challenge."""

import math

import numpy as np

from swarmsim.metrics.Circliness import Circliness
from swarmsim.metrics.Metric import Metric


class ChallengeScore(Metric):
    """Track delivery quality for the defender swarm on every world step."""

    def __init__(self, name="ChallengeScore"):
        super().__init__(name=name)
        self.circliness_metric = Circliness(history=1, avg_history_max=1)
        self.reset()

    def reset(self):
        super().reset()
        self.centroid = None
        self.target_distance = None
        self.circliness = None
        self.finalized = False
        self.completion_step = None
        self.completion_time = None
        self.final_score = None
        self.best_score = math.inf

    def attach_world(self, world):
        super().attach_world(world)
        self.start = np.asarray(world.meta["start"], dtype=float)
        self.target = np.asarray(world.meta["target"], dtype=float)
        stop_score = world.meta.get("stop_score")
        self.automatic_stop_score = None if stop_score is None else float(stop_score)
        self.circliness_metric.world_radius = world.config.radius

    @property
    def defenders(self):
        return [agent for agent in self.world.population if agent.team == "defender"]

    def calculate(self):
        if self.finalized:
            return

        defenders = self.defenders
        if not defenders:
            return

        positions = np.asarray([agent.getPosition() for agent in defenders], dtype=float)
        self.centroid = positions.mean(axis=0)
        self.target_distance = float(np.linalg.norm(self.centroid - self.target))

        self.circliness_metric.population = defenders
        self.circliness_metric.calculate()
        self.circliness = float(np.clip(self.circliness_metric.value, 0.0, 1.0))

        score = self.target_distance + 1.0 - self.circliness
        self.set_value(score)

        if score < self.best_score:
            self.best_score = score

        if self.automatic_stop_score is not None and score <= self.automatic_stop_score:
            self.finalize()

    def finalize(self):
        """Record the official result at the current simulation step."""
        if self.finalized:
            return

        if self.value is None:
            self.calculate()
        if self.value is None:
            return

        self.finalized = True
        self.completion_step = self.world.total_steps
        self.completion_time = self.simulation_time
        self.final_score = float(self.value)

    @property
    def simulation_time(self):
        return self.world.total_steps * self.world.dt

    @property
    def minimum_score(self):
        return None if self.best_score == math.inf else self.best_score
