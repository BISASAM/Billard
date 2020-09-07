import pygame
from titlescene import TitleScene
from gamescene import GameScene


def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    active_scene = starting_scene(screen)

    while active_scene != None:
        elapsed_time = clock.tick(fps)
        pressed_keys = pygame.key.get_pressed()

        # filter events
        filtered_events = []
        for event in pygame.event.get():
            # check for quit attempt
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update(elapsed_time)
        active_scene.Render()

        active_scene = active_scene.next

        pygame.display.flip()


if __name__ == "__main__":
    run_game(1680, 880, 240, GameScene)
