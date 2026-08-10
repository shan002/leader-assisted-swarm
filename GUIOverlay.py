"""Challenge-specific display layered on top of the Swarmsim world."""

import numpy as np
import pygame

from swarmsim.gui.agentGUI import get_font


GOLD = (255, 215, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


class GUIOverlay:
    def __init__(self, world, score):
        self.world = world
        self.score = score
        self.font = None

    def screen_position(self, position):
        point = np.asarray(position) * self.world.zoom + self.world.pos
        return tuple(np.rint(point).astype(int))

    @staticmethod
    def draw_symbol(surface, center, color, radius=7):
        x, y = center
        pygame.draw.circle(surface, (0, 0, 0), center, radius + 4, width=4)
        pygame.draw.circle(surface, color, center, radius, width=2)
        pygame.draw.line(surface, color, (x - radius - 4, y), (x + radius + 4, y), width=2)
        pygame.draw.line(surface, color, (x, y - radius - 4), (x, y + radius + 4), width=2)

    def draw_world_symbol(self, screen, position, color, radius=7):
        if position is not None:
            self.draw_symbol(screen, self.screen_position(position), color, radius)

    @staticmethod
    def number(value):
        return "--" if value is None else f"{value:.4f}"

    def draw_panel(self, screen):
        if self.score.finalized:
            status = self.score.outcome
            action_text = "Press R to restart or Q to quit"
        else:
            status = "SEARCHING"
            action_text = "Guide the swarm to the evader"
        lines = [
            f"Status: {status}",
            f"Seed: {self.world.config.seed}",
            f"Time: {self.score.simulation_time:.2f} s",
            f"Final score: {self.number(self.score.final_score)}",
            f"Evader distance: {self.number(self.score.evader_distance)}",
            f"Evader to goal: {self.number(self.score.evader_goal_distance)}",
            f"Circliness: {self.number(self.score.circliness)}",
            f"Evader caught: {'YES' if self.score.caught else 'NO'}",
            action_text,
        ]
        if self.score.catcher_name is not None:
            lines.insert(-1, f"Caught by: defender {self.score.catcher_name}")
        legend = [(RED, "Protected point"), (GOLD, "Swarm centroid")]

        row_height = self.font.get_linesize()
        padding = 10
        icon_space = 28
        text_width = max(self.font.size(line)[0] for line in lines)
        legend_width = max(icon_space + self.font.size(label)[0] for _, label in legend)
        width = max(text_width, legend_width) + 2 * padding
        height = (len(lines) + len(legend) + 1) * row_height + 2 * padding + 10
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 185))

        y = padding
        for line in lines:
            panel.blit(self.font.render(line, True, WHITE), (padding, y))
            y += row_height

        pygame.draw.line(panel, (130, 130, 130), (padding, y + 3), (width - padding, y + 3))
        y += 10

        panel.blit(self.font.render("Legend", True, WHITE), (padding, y))
        y += row_height

        for color, label in legend:
            symbol_center = (padding + 8, y + row_height // 2)
            self.draw_symbol(panel, symbol_center, color, radius=5)
            panel.blit(self.font.render(label, True, WHITE), (padding + icon_space, y))
            y += row_height

        screen.blit(panel, (10, 10))

    def draw(self, screen):
        if self.font is None:
            self.font = get_font("JetBrainsMono-SemiBold.ttf", 14)

        self.draw_world_symbol(screen, self.score.protected_point, RED, radius=9)
        self.draw_world_symbol(screen, self.score.centroid, GOLD)
        self.draw_panel(screen)


def add_gui_overlay(world, score):
    overlay = GUIOverlay(world, score)
    original_draw = world.draw

    def draw(screen, offset=None):
        original_draw(screen, offset)
        overlay.draw(screen)

    world.draw = draw
    return overlay
