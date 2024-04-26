import tkinter as tk
import math


class Vector2D:
    def __init__(self, x, y) -> None:
        """
        Initializes the 2D vector
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Vector2D':
        """
        Adds two vectors
        :param other:
        :return:
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> 'Vector2D':
        """
        Subtracts two vectors
        :param other:
        :return:
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def __truediv__(self, other) -> 'Vector2D':
        """
        Divides two vectors
        :param other:
        :return:
        """
        return Vector2D(self.x / other, self.y / other)

    def __str__(self) -> str:
        """
        Returns the string representation of the vector
        :return:
        """
        return f"({self.x}, {self.y})"


class Bullet:
    def __init__(self, position, velocity, direction):
        self.position = position
        self.velocity = velocity
        self.direction = direction
        self.length = 10

    def update(self, canvas: tk.Canvas) -> bool:
        rotated_direction = (self.direction + 90) % 360
        end_point = Vector2D(
            self.position.x + self.length * math.cos(math.radians(rotated_direction)),
            self.position.y + self.length * math.sin(math.radians(rotated_direction))
        )
        canvas.create_line(self.position.x, self.position.y, end_point.x, end_point.y, fill="white")
        self.position = Vector2D(
            (self.position.x + self.velocity.x),
            (self.position.y + self.velocity.y)
        )
        if (self.position.x < 0 or self.position.x > canvas.winfo_width() or
                self.position.y < 0 or self.position.y > canvas.winfo_height()):
            return False
        else:
            return True


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
        bullet_speed = 10  # Set a constant speed for the bullet
        bullet_velocity = Vector2D(
            bullet_speed * math.sin(math.radians(self.direction)),
            -bullet_speed * math.cos(math.radians(self.direction))
        )
        bullet = Bullet(Vector2D(self.position.x, self.position.y), bullet_velocity, self.direction)
        self.bullets.append(bullet)

    def rotate(self, angle: int) -> None:
        self.direction += angle


class Wrapper:
    def __init__(self, width: int = 800, height: int = 600):
        self.player = Player(Vector2D(width / 2, height / 2), Vector2D(0, 0), 0, 1, width, height)
        self.score = 0

        self.root: tk.Tk = tk.Tk()
        self.root.title("Wrapper")
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.keys_pressed = {}

        self.main_canvas: tk.Canvas = tk.Canvas(self.root, width=width, height=height, bg="black")
        self.main_canvas.pack()

    def on_key_press(self, event: tk.Event) -> None:
        self.keys_pressed[event.keysym] = True

    def on_key_release(self, event: tk.Event) -> None:
        self.keys_pressed[event.keysym] = False

    def update_score(self) -> None:
        self.main_canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 16))

    def update(self) -> None:
        if self.keys_pressed.get("Escape") or self.keys_pressed.get("q"):
            self.root.quit()
        if self.keys_pressed.get("Up"):
            self.player.accelerate(1)
        if self.keys_pressed.get("Down"):
            self.player.accelerate(-1)
        if self.keys_pressed.get("Left"):
            self.player.rotate(-5)
        if self.keys_pressed.get("Right"):
            self.player.rotate(5)
        if self.keys_pressed.get("space"):
            self.player.shoot(self.main_canvas)

        self.main_canvas.delete("all")
        self.update_score()
        self.player.update(self.main_canvas)
        self.root.update()
        self.root.after(50, self.update)

    def run(self):
        self.root.after(0, self.update)
        self.root.mainloop()
