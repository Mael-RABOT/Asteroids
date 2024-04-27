import math
import tkinter as tk

from Bullet import Bullet
from Vector2D import Vector2D

MAX_BULLETS = 5
COOLDOWN = 10


class Player:
    def __init__(self, position: Vector2D, velocity: Vector2D, direction: int, size: int = 2, screen_width: int = 800, screen_height: int = 600) -> None:
        self.position = position
        self.velocity = velocity
        self.direction = direction
        self.size = size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_speed = 10
        self.bullets = []
        self.shoot_cooldown = 0

    def update(self, canvas: tk.Canvas) -> None:
        self.position = Vector2D((self.position.x + self.velocity.x) % self.screen_width, (self.position.y + self.velocity.y) % self.screen_height)

        triangle = [
            (self.position.x, self.position.y - 10 * self.size),
            (self.position.x - 5 * self.size, self.position.y + 10 * self.size),
            (self.position.x + 5 * self.size, self.position.y + 10 * self.size),
        ]

        theta = math.radians(self.direction)
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        triangle = [
            (
                cos_theta * (x - self.position.x) - sin_theta * (y - self.position.y) + self.position.x,
                sin_theta * (x - self.position.x) + cos_theta * (y - self.position.y) + self.position.y,
            )
            for x, y in triangle
        ]

        canvas.create_polygon(triangle, fill="white")

        self.bullets = [bullet for bullet in self.bullets if bullet.update(canvas)]

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def accelerate(self, acceleration: int) -> None:
        new_velocity = Vector2D(
            self.velocity.x + acceleration * math.sin(math.radians(self.direction)),
            self.velocity.y - acceleration * math.cos(math.radians(self.direction)),
            )
        speed = math.sqrt(new_velocity.x**2 + new_velocity.y**2)
        if speed > self.max_speed:
            new_velocity = Vector2D(new_velocity.x * self.max_speed / speed, new_velocity.y * self.max_speed / speed)
        self.velocity = new_velocity

    def shoot(self, canvas: tk.Canvas) -> None:
        if len(self.bullets) > MAX_BULLETS or self.shoot_cooldown > 0:
            return

        bullet_speed = 10
        bullet_velocity = Vector2D(
            bullet_speed * math.sin(math.radians(self.direction)),
            -bullet_speed * math.cos(math.radians(self.direction))
        )
        bullet = Bullet(Vector2D(self.position.x, self.position.y), bullet_velocity, self.direction)
        self.bullets.append(bullet)
        self.shoot_cooldown = COOLDOWN

    def rotate(self, angle: int) -> None:
        self.direction += angle
