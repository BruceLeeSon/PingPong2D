import random
import time
import arcade
from pyglet.event import EVENT_HANDLE_STATE

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "PING PONG TABLE"
SPEED_X = 5
SPEED_Y = -7
SPEED_BAR = 6.4


class Ball(arcade.Sprite):
    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right > SCREEN_WIDTH or self.left < 0:
            self.change_x = -self.change_x
        if self.top > SCREEN_HEIGHT or self.bottom < 0:
            self.change_y = -self.change_y


class Bar(arcade.Sprite):
    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width=width, height=height, title=title)

        self.ball = Ball("ball.png", 0.1)

        self.bar = Bar("bar.png", 0.1)
        self.setup()
        self.score = 0
        self.attempts = 3
        self.is_active = True

    def setup(self):
        self.ball.center_x = SCREEN_WIDTH / 2
        self.ball.center_y = SCREEN_HEIGHT / 2
        self.ball.change_x = SPEED_X
        self.ball.change_y = SPEED_Y

        self.bar.center_x = SCREEN_WIDTH / 2
        self.bar.center_y = SCREEN_HEIGHT * 4 / 100
        direction = random.randint(1, 2)
        time.sleep(1)
        if direction < 2:
            self.ball.change_x = -SPEED_X
        else:
            self.ball.change_x = SPEED_X
            self.ball.change_y = SPEED_Y
            self.bar.center_x = SCREEN_WIDTH / 2

    def on_update(self, delta_time: float) -> bool | None:
        self.ball.update()
        self.bar.update()
        if arcade.check_for_collision(self.bar, self.ball):
            self.ball.bottom = self.bar.top + 1
            self.ball.change_y = -self.ball.change_y
            self.score += 1
        if self.ball.bottom < 0:
            self.attempts -= 1
            self.setup()
        if self.attempts == 0:
            self.is_active = False
        if not self.is_active:
            self.ball.stop()
            self.bar.stop()

    def on_draw(self):
        self.clear((100, 149, 237))
        arcade.draw_sprite(self.ball)
        arcade.draw_sprite(self.bar)
        arcade.draw_text(f"Score: {self.score}", 20, SCREEN_HEIGHT - 30, (0, 0, 0), 20)
        arcade.draw_text(f"Attempts: {self.attempts}", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30, (0, 0, 0), 20)
        if self.attempts == 0:
            arcade.draw_text("Defeat!", 0, SCREEN_HEIGHT / 2, (255, 0, 0), 50, SCREEN_WIDTH, "center",
                             font_name="Montserrat")
        if self.score >= 20:
            arcade.draw_text("Winnnnn!", 0, SCREEN_HEIGHT / 2, (0, 255, 127), 50, SCREEN_WIDTH, "center",
                             font_name="Montserrat")
            self.is_active = False

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if self.is_active == True:
            if symbol == arcade.key.LEFT:
                self.bar.change_x = -SPEED_BAR
            if symbol == arcade.key.RIGHT:
                self.bar.change_x = SPEED_BAR

    def on_key_release(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if self.is_active == True:
            if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
                self.bar.change_x = 0


game = Game(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)

arcade.run()
