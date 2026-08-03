"""Leader controller submission for the automated leader challenge.
"""

from swarmsim.agent.control.AbstractController import AbstractController


class LeaderController(AbstractController):
    """Starter controller for the informed leader."""

    def __init__(self, agent=None, parent=None, max_speed=0.3, max_turn_rate=1.5):
        super().__init__(agent=agent, parent=parent)
        self.max_speed = float(max_speed)
        self.max_turn_rate = float(max_turn_rate)

    def get_actions(self, agent):
        """Return ``(linear_velocity, angular_velocity)`` for the leader.

        Useful information is available through:

        - ``agent.pos`` and ``agent.angle`` for the leader state
        - ``agent.world.population`` for all agents
        - ``agent.world.meta["target"]`` for the destination

        The starter controller moves the leader straight ahead.
        """
        linear_velocity = 0.2
        angular_velocity = 0.0
        return linear_velocity, angular_velocity
