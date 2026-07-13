from swarmsim.world.RectangularWorld import RectangularWorld, RectangularWorldConfig
from swarmsim.world.simulate import main as sim


world_config = RectangularWorldConfig.from_yaml("world.yaml")
world = RectangularWorld(world_config)
sim(world)