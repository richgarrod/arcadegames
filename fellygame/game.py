import arcade
import random
import time
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5

class FailedIt(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)

    def __init__(self):
        super().__init__()
        self.fail_text = "YOU FAILED. LOSER!"

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.fail_text, 50, 200, arcade.color.WHITE, 25)

    def on_key_press(self, key, modifiers):
        arcade.close_window()

class NailedIt(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.APPLE_GREEN)

    def __init__(self):
        super().__init__()
        self.success_text = "YOU FUCKING NAILED IT YOU ABSOLUTE HERO"

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.success_text, 50, 200, arcade.color.RED, 25)

    def on_key_press(self, key, modifiers):
        arcade.close_window()

class MyGame(arcade.View):
    """ Main application class. """

    def on_show(self):
        arcade.set_background_color(arcade.color.ASH_GREY)

    def __init__(self):
        super().__init__()
        self.score = 0
        self.end_text = ""
        self.old_paul_x = -1
        self.old_paul_y = -1
        self.shoes = arcade.SpriteList()
        self.felly = arcade.Sprite('images/felly.png', 0.2)
        self.felly.center_x = 400
        self.felly.center_y = 300
        self.paul = arcade.Sprite('images/paul.png', 0.2)
        self.paul.center_x = random.randrange(0, SCREEN_WIDTH-10)
        self.paul.center_y = random.randrange(0, SCREEN_HEIGHT-10)
        self.walls = arcade.SpriteList()
        self.create_walls()
        for i in range(0, 100):
            shoe = arcade.Sprite('images/shoe.png', 0.1)
            shoe.center_x = random.randrange(0, SCREEN_WIDTH-10)
            shoe.center_y = random.randrange(0, SCREEN_HEIGHT-10)
            self.shoes.append(shoe)
        self.physics_engine = arcade.PhysicsEngineSimple(self.felly, self.walls)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.paul, self.walls)

    def create_walls(self):
        for i in range(0, SCREEN_WIDTH):
            wall = arcade.Sprite('images/wall.png', 0.1)
            wall.center_y = 0
            wall.center_x = i
            self.walls.append(wall)
        for i in range(0, SCREEN_WIDTH):
            wall = arcade.Sprite('images/wall.png', 0.1)
            wall.center_y = SCREEN_HEIGHT
            wall.center_x = i
            self.walls.append(wall)
        for i in range(0, SCREEN_HEIGHT):
            wall = arcade.Sprite('images/wall.png', 0.1)
            wall.center_x = 0
            wall.center_y = i
            self.walls.append(wall)
        for i in range(0, SCREEN_HEIGHT):
            wall = arcade.Sprite('images/wall.png', 0.1)
            wall.center_x = SCREEN_WIDTH
            wall.center_y = i
            self.walls.append(wall)


    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        self.felly.draw()
        self.shoes.draw()
        self.walls.draw()
        self.paul.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.shoes.update()
        collisions = arcade.check_for_collision_with_list(self.felly, self.shoes)
        for collision in collisions:
            self.score += 1
            collision.kill()
        dead_collision = arcade.check_for_collision(self.felly, self.paul)
        if dead_collision:
            failed_it = FailedIt()
            self.window.show_view(failed_it)
        if self.score == 100:
            nailed_it = NailedIt()
            self.window.show_view(nailed_it)
        self.move_paul()
        self.physics_engine.update()
        self.physics_engine2.update()

    def move_paul(self):
        felly_coords = self.felly.position
        paul_coords = self.paul.position
        diff_x = felly_coords[0] - paul_coords[0]
        diff_y = felly_coords[1] - paul_coords[1]
        if diff_y == 0:
            self.paul.change_x = 0
        elif diff_x > 0:
            self.paul.change_x = min((math.fabs(diff_x) / math.fabs(diff_y)), 2)
        else:
            self.paul.change_x = -1 * min((math.fabs(diff_x) / math.fabs(diff_y)), 2)
        if diff_x == 0:
            self.paul.change_y = 0
        elif diff_y > 0:
            self.paul.change_y = min((math.fabs(diff_y) / math.fabs(diff_x)), 2)
        else:
            self.paul.change_y = -1 * min((math.fabs(diff_y) / math.fabs(diff_x)), 2)

        print(self.paul.change_x)
        print(self.paul.change_y)



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.felly.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.felly.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.felly.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.felly.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.felly.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.felly.change_x = 0

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    game = MyGame()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()

