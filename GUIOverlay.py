import math

import numpy as np
import pygame

from swarmsim.gui.agentGUI import get_font
from swarmsim.metrics.Circliness import Circliness


GOAL = np.array([5.0, 5.0])
MERGE_DISTANCE = 2.0

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)


class GUIOverlay:
    def __init__(self, world):
        self.world = world
        self.metric = Circliness(history=1, avg_history_max=1)

        self.cm_a = self.cm_b = self.cm_all = None
        self.goal_distance = self.circliness = self.loss = None

        self.minimum_loss = math.inf
        self.merged = False
        self.last_step = None
        self.font = None

    @staticmethod
    def color(agent):
        color = getattr(agent, "body_color", None)
        return None if color is None else tuple(map(int, color[:3]))

    def agents_with_color(self, color):
        return [
            agent
            for agent in self.world.population
            if self.color(agent) == color
        ]

    def center_of_mass(self, agents):
        if not agents:
            return None

        # Circliness inherits center_of_mass() from RadialVarianceMetric.
        self.metric.population = agents
        return self.metric.center_of_mass()

    @staticmethod
    def groups_are_merged(agents):
        if len(agents) < 2:
            return False

        positions = np.array([
            agent.getPosition()
            for agent in agents
        ])

        distances = np.linalg.norm(
            positions[:, None] - positions[None, :],
            axis=2,
        )

        connected = distances <= MERGE_DISTANCE
        reached = {0}

        while True:
            new = set(
                np.where(
                    connected[list(reached)].any(axis=0)
                )[0]
            )

            if new <= reached:
                return len(reached) == len(agents)

            reached |= new

    def update(self):
        step = getattr(self.world, "total_steps", 0)

        # Prevent repeated metric updates during the same simulation step.
        if step == self.last_step:
            return

        self.last_step = step

        group_a = self.agents_with_color(RED)
        group_b = self.agents_with_color(BLUE)
        swarm = group_a + group_b

        self.cm_a = self.center_of_mass(group_a)
        self.cm_b = self.center_of_mass(group_b)
        self.cm_all = self.center_of_mass(swarm)

        self.merged = self.groups_are_merged(swarm)

        # Loss is only shown after the two groups merge.
        if not self.merged:
            self.goal_distance = None
            self.circliness = None
            self.loss = None
            return

        self.goal_distance = float(
            np.linalg.norm(self.cm_all - GOAL)
        )

        self.metric.population = swarm
        self.metric.calculate()

        self.circliness = float(
            np.clip(self.metric.value, 0.0, 1.0)
        )

        # loss = distance to endpoint + milling loss
        self.loss = (
            self.goal_distance
            + 1.0
            - self.circliness
        )

        self.minimum_loss = min(
            self.minimum_loss,
            self.loss,
        )

    def screen_position(self, position):
        point = (
            np.asarray(position) * self.world.zoom
            + self.world.pos
        )

        return tuple(np.rint(point).astype(int))

    @staticmethod
    def draw_symbol(
        surface,
        center,
        color,
        radius=6,
        outline=False,
    ):
        x, y = center

        if outline:
            pygame.draw.circle(
                surface,
                (0, 0, 0),
                center,
                radius + 4,
                width=4,
            )

        pygame.draw.circle(
            surface,
            color,
            center,
            radius,
            width=2,
        )

        pygame.draw.line(
            surface,
            color,
            (x - radius - 4, y),
            (x + radius + 4, y),
            width=2,
        )

        pygame.draw.line(
            surface,
            color,
            (x, y - radius - 4),
            (x, y + radius + 4),
            width=2,
        )

    def draw_world_symbol(
        self,
        screen,
        position,
        color,
        radius=7,
    ):
        if position is None:
            return

        self.draw_symbol(
            screen,
            self.screen_position(position),
            color,
            radius,
            outline=True,
        )

    @staticmethod
    def number(value):
        return "--" if value is None else f"{value:.4f}"

    def legend(self):
        if self.merged:
            return [
                (GOLD, "Combined CM"),
                (WHITE, "End point"),
            ]

        return [
            (RED, "Group A CM"),
            (BLUE, "Group B CM"),
            (WHITE, "End point"),
        ]

    def draw_panel(self, screen):
        best = (
            None
            if self.minimum_loss == math.inf
            else self.minimum_loss
        )

        lines = [
            f"Status: {'MERGED' if self.merged else 'SEPARATE'}",
            f"Current loss: {self.number(self.loss)}",
            f"Minimum loss: {self.number(best)}",
            f"Goal distance: {self.number(self.goal_distance)}",
            f"Circliness: {self.number(self.circliness)}",
        ]

        legend = self.legend()

        row_height = self.font.get_linesize()
        padding = 10
        icon_space = 28

        text_width = max(
            self.font.size(text)[0]
            for text in lines
        )

        legend_width = max(
            icon_space + self.font.size(text)[0]
            for _, text in legend
        )

        width = max(
            text_width,
            legend_width,
        ) + 2 * padding

        height = (
            (len(lines) + len(legend) + 1)
            * row_height
            + 2 * padding
            + 10
        )

        panel = pygame.Surface(
            (width, height),
            pygame.SRCALPHA,
        )

        panel.fill((0, 0, 0, 185))

        y = padding

        for text in lines:
            panel.blit(
                self.font.render(
                    text,
                    True,
                    WHITE,
                ),
                (padding, y),
            )

            y += row_height

        pygame.draw.line(
            panel,
            (130, 130, 130),
            (padding, y + 3),
            (width - padding, y + 3),
        )

        y += 10

        panel.blit(
            self.font.render(
                "Legend",
                True,
                WHITE,
            ),
            (padding, y),
        )

        y += row_height

        for color, text in legend:
            symbol_center = (
                padding + 8,
                y + row_height // 2,
            )

            self.draw_symbol(
                panel,
                symbol_center,
                color,
                radius=5,
            )

            panel.blit(
                self.font.render(
                    text,
                    True,
                    WHITE,
                ),
                (padding + icon_space, y),
            )

            y += row_height

        screen.blit(panel, (10, 10))

    def draw(self, screen):
        if self.font is None:
            self.font = get_font(
                "JetBrainsMono-SemiBold.ttf",
                14,
            )

        self.update()

        # End point
        self.draw_world_symbol(
            screen,
            GOAL,
            WHITE,
            radius=9,
        )

        # Center-of-mass markers
        if self.merged:
            self.draw_world_symbol(
                screen,
                self.cm_all,
                GOLD,
            )
        else:
            self.draw_world_symbol(
                screen,
                self.cm_a,
                RED,
            )

            self.draw_world_symbol(
                screen,
                self.cm_b,
                BLUE,
            )

        self.draw_panel(screen)


def add_gui_overlay(world):
    overlay = GUIOverlay(world)
    original_draw = world.draw

    def draw(screen, offset=None):
        original_draw(screen, offset)
        overlay.draw(screen)

    world.draw = draw
    return overlay