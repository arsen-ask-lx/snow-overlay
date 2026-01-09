import random
import math


class Snowflake:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset(initial=True)

    def reset(self, initial=False):
        self.x = random.uniform(0, self.screen_width)
        if initial:
            self.y = random.uniform(-self.screen_height, self.screen_height)
        else:
            self.y = random.uniform(-self.screen_height, 0)
        self.size = random.uniform(1.0, 4.0)
        self.fall_speed = random.uniform(1.0, 3.0)
        self.sway_amplitude = random.uniform(0.5, 2.0)
        self.sway_frequency = random.uniform(0.02, 0.05)
        self.sway_offset = random.uniform(0, 2 * math.pi)
        self.opacity = random.uniform(0.4, 0.9)

    def update(self, time_delta, frame_count):
        self.y += self.fall_speed * time_delta
        self.x += (
            math.sin(frame_count * self.sway_frequency + self.sway_offset)
            * self.sway_amplitude
        )

        if self.y > self.screen_height + self.size:
            self.reset()

    def update_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
