from swarmsim.world.RectangularWorld import RectangularWorld, RectangularWorldConfig
from swarmsim.world.simulate import main as sim

from GUIOverlay import add_gui_overlay


world_config = RectangularWorldConfig.from_yaml("world.yaml")
world = RectangularWorld(world_config)

add_gui_overlay(world)
sim(world)