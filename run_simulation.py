"""Run and score the leader-assisted evader capture challenge."""

import argparse
import secrets

import pygame

from swarmsim import register_dictlike_type
from swarmsim.world.RectangularWorld import RectangularWorld, RectangularWorldConfig
from swarmsim.world.simulate import main as simulate
from swarmsim.world.spawners.AgentSpawner import UniformAgentSpawner

from GUIOverlay import add_gui_overlay
from leader_controller import LeaderController
from scoring import ChallengeScore


class ProtectedPointSpawner(UniformAgentSpawner):
    def set_angle_post_spawn(self, agent):
        agent.angle = self.angle_between(agent.pos, self.world.meta["protected_point"])


def build_world(seed=None):
    register_dictlike_type("controller", "LeaderController", LeaderController)
    register_dictlike_type("spawners", "ProtectedPointSpawner", ProtectedPointSpawner)
    config = RectangularWorldConfig.from_yaml("world.yaml")
    if seed is not None:
        config.seed = seed
    world = RectangularWorld(config)
    score = world.add_metric(ChallengeScore())
    add_gui_overlay(world, score)
    return world, score


def print_result(world, score):
    def number(value):
        return "--" if value is None else f"{value:.4f}"

    print()
    print("LEADER-ASSISTED EVADER CAPTURE")
    print(f"Seed: {world.config.seed}")
    if score.finalized:
        print(f"Status: {score.outcome}")
        print(f"Time: {score.final_time:.2f} simulation seconds")
        print(f"Score: {score.final_score:.4f}")
        print(f"Circliness: {score.circliness:.4f}")
        print(f"Final step: {score.final_step}")
        if score.catcher_name is not None:
            print(f"Caught by: defender {score.catcher_name}")
    else:
        print("Status: CLOSED WITHOUT FINALIZING")
        print(f"Time: {world.total_steps * world.dt:.2f} simulation seconds")
        print(f"Evader distance: {number(score.evader_distance)}")
        print(f"Final circliness: {number(score.circliness)}")


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
        elif event.key == pygame.K_q:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif event.key == pygame.K_r and score.finalized:
            control_state["restart"] = True
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            original_handle_key_press(event)

    world.handle_key_press = handle_key_press

    def keep_window_open(_world):
        if score.finalized:
            request_pause()
        return False

    control_state["restart"] = False
    return keep_window_open, control_state


def parse_args():
    parser = argparse.ArgumentParser(description="Run the leader-assisted evader capture challenge.")
    parser.add_argument("--start_paused", action="store_true", help="open the simulation in a paused state")
    parser.add_argument("--seed", type=int, help="seed for the first run (default: random)")
    return parser.parse_args()


def main():
    args = parse_args()
    seed = secrets.randbits(31) if args.seed is None else args.seed
    while True:
        world, score = build_world(seed)
        keep_window_open, control_state = add_challenge_controls(world, score, start_paused=args.start_paused)
        simulate(
            world,
            stop_detection=keep_window_open,
            start_paused=args.start_paused,
            world_key_events=True,
        )
        print_result(world, score)
        if not control_state["restart"]:
            break
        seed = (seed + 1) % (2 ** 31)


if __name__ == "__main__":
    main()
