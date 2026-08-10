"""Scoring for the leader-assisted evader capture challenge."""

import numpy as np

from swarmsim.metrics.Circliness import Circliness
from swarmsim.metrics.Metric import Metric


class ChallengeScore(Metric):
    def __init__(self, name="ChallengeScore"):
        super().__init__(name=name)
        self.circliness_metric = Circliness(history=1, avg_history_max=1)
        self.reset()

    def reset(self):
        super().reset()
        self.centroid = None
        self.evader_distance = None
        self.evader_goal_distance = None
        self.circliness = None
        self.caught = False
        self.catcher_name = None
        self.outcome = None
        self.finalized = False
        self.final_step = None
        self.final_time = None
        self.final_score = None

    def attach_world(self, world):
        super().attach_world(world)
        self.protected_point = np.asarray(world.meta["protected_point"], dtype=float)
        self.protected_radius = float(world.meta.get("protected_radius", 0.2))
        self.circliness_metric.world_radius = world.config.radius

    @property
    def defenders(self):
        return [agent for agent in self.world.population if agent.team == "defender"]

    @property
    def evader(self):
        return next((agent for agent in self.world.population if agent.team == "evader"), None)

    @staticmethod
    def touching_defender(defenders, evader):
        evader_collisions = getattr(evader, "collided", ())
        return next((defender for defender in defenders
                     if evader in getattr(defender, "collided", ())
                     or defender in evader_collisions), None)

    def calculate(self):
        if self.finalized:
            return

        defenders = self.defenders
        evader = self.evader
        if not defenders or evader is None:
            return

        positions = np.asarray([defender.getPosition() for defender in defenders], dtype=float)
        self.centroid = positions.mean(axis=0)
        self.evader_distance = float(np.linalg.norm(self.centroid - evader.getPosition()))
        self.evader_goal_distance = float(np.linalg.norm(evader.getPosition() - self.protected_point))

        self.circliness_metric.population = defenders
        self.circliness_metric.calculate()
        self.circliness = float(np.clip(self.circliness_metric.value, 0.0, 1.0))

        catcher = self.touching_defender(defenders, evader)
        self.caught = catcher is not None
        if self.caught:
            self.catcher_name = catcher.name
            self.finalize("CAUGHT", self.simulation_time + 1.0 - self.circliness)
        elif self.evader_goal_distance <= self.protected_radius:
            self.finalize("MISSED", self.simulation_time + 2.0)
        else:
            self.set_value(self.simulation_time + 1.0 - self.circliness)

    def finalize(self, outcome, score):
        if self.finalized:
            return
        self.finalized = True
        self.outcome = outcome
        self.final_step = self.world.total_steps
        self.final_time = self.simulation_time
        self.final_score = float(score)
        self.set_value(self.final_score)

    @property
    def simulation_time(self):
        return self.world.total_steps * self.world.dt
