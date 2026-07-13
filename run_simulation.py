from swarmsim.world.RectangularWorld import RectangularWorld, RectangularWorldConfig
from swarmsim.agent.StaticAgent import StaticAgent
from swarmsim.world.simulate import main as sim
from swarmsim.config import register_dictlike_type
from RCController import RCController
from GoalSeekingController import GoalSeekingController
from BinaryPriorityController import BinaryPriorityController


register_dictlike_type("controller", "RCController", RCController)
register_dictlike_type("controller", "GoalSeekingController", GoalSeekingController)
register_dictlike_type("controller", "BinaryPriorityController", BinaryPriorityController)
world_config = RectangularWorldConfig.from_yaml("world.yaml")
world = RectangularWorld(world_config)
sim(world)