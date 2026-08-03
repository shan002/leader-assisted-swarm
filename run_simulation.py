"""Run and score the automated leader challenge."""

import argparse

import pygame

from swarmsim import register_dictlike_type
from swarmsim.world.RectangularWorld import RectangularWorld, RectangularWorldConfig
from swarmsim.world.simulate import main as simulate

from GUIOverlay import add_gui_overlay
from leader_controller import LeaderController
from scoring import ChallengeScore


def build_world():
    register_dictlike_type("controller", "LeaderController", LeaderController)
    config = RectangularWorldConfig.from_yaml("world.yaml")
    world = RectangularWorld(config)
    score = world.add_metric(ChallengeScore())
    add_gui_overlay(world, score)
    return world, score


def print_result(world, score):
    def number(value):
        return "--" if value is None else f"{value:.4f}"

    print()
    print("AUTOMATED LEADER CHALLENGE")
    if score.finalized:
        print("Status: FINALIZED")
        print(f"Time: {score.completion_time:.2f} simulation seconds")
        print(f"Score: {score.final_score:.4f}")
        print(f"Minimum score: {score.minimum_score:.4f}")
        print(f"Final step: {score.completion_step}")
    else:
        print("Status: CLOSED WITHOUT FINALIZING")
        print(f"Time: {world.total_steps * world.dt:.2f} simulation seconds")
        print(f"Final distance: {number(score.target_distance)}")
        print(f"Final circliness: {number(score.circliness)}")
        print(f"Minimum score: {number(score.minimum_score)}")


def add_challenge_controls(world, score, start_paused=False):
    original_handle_key_press = world.handle_key_press
    control_state = {"paused": start_paused, "pause_requested": False}

    def request_pause():
        if control_state["paused"] or control_state["pause_requested"]:
            return
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        control_state["pause_requested"] = True

    def handle_key_press(event):
        if event.key == pygame.K_SPACE:
            control_state["paused"] = not control_state["paused"]
            control_state["pause_requested"] = False
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            score.finalize()
            request_pause()
        elif event.key == pygame.K_q:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            original_handle_key_press(event)

    world.handle_key_press = handle_key_press

    def keep_window_open(_world):
        if score.finalized:
            request_pause()
        return False

    return keep_window_open


def parse_args():
    parser = argparse.ArgumentParser(description="Run the automated leader challenge.")
    parser.add_argument("--start_paused", action="store_true", help="open the simulation in a paused state")
    return parser.parse_args()


def main():
    args = parse_args()
    world, score = build_world()
    keep_window_open = add_challenge_controls(world, score, start_paused=args.start_paused)
    simulate(
        world,
        stop_detection=keep_window_open,
        start_paused=args.start_paused,
        world_key_events=True,
    )
    print_result(world, score)


if __name__ == "__main__":
    main()
