"""Leader controller submission for the evader capture challenge."""

from swarmsim.agent.control.AbstractController import AbstractController


class LeaderController(AbstractController):
    """Controller for the informed leader."""

    def __init__(self, agent=None, parent=None, max_speed=0.1, max_turn_rate=1.5):
        super().__init__(agent=agent, parent=parent)
        self.max_speed = float(max_speed)
        self.max_turn_rate = float(max_turn_rate)

    def get_actions(self, agent):
        """Return the leader's forward and angular velocities."""
        # All agents are available through agent.world.population.
        # Their team is "defender", "leader", or "evader".
        linear_velocity = self.max_speed
        angular_velocity = 0.0
        return linear_velocity, angular_velocity
