import arcade
import random
import math
from fail_view import FailedIt
from nail_view import NailedIt
from utils import create_walls

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5
BADDY_SPEED = 2
LEMON_COUNT = 10
SHOE_COUNT = 100

class MyGame(arcade.View):
    """ Main application class. """

    def on_show(self):
        arcade.set_background_color(arcade.color.ASH_GREY)

    def __init__(self):
        super().__init__()
        self.score = 0
        self.end_text = ""
        self.shoes = arcade.SpriteList()
        self.lemons = arcade.SpriteList()
        self.baddies = arcade.SpriteList()
        self.lemon_count = LEMON_COUNT
        self.felly = arcade.Sprite('images/felly.png', 0.2)
        self.felly.center_x = 400
        self.felly.center_y = 300
        self.paul = arcade.Sprite('images/paul.png', 0.2)
        self.paul.center_x, self.paul.center_y = self.get_acceptable_coordinates()
        self.baddies.append(self.paul)
        self.baddybadguy = arcade.Sprite('images/baddybadguy.png', 0.2)
        self.baddybadguy.center_x, self.baddybadguy.center_y = self.get_acceptable_coordinates()
        self.baddies.append(self.baddybadguy)
        self.walls = create_walls(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.felly_speed = 5
        self.baddy_speed = 2
        self.baddy_speed = 2
        self.counter = 0
        self.multiplier = 1
        for i in range(SHOE_COUNT):
            shoe = arcade.Sprite('images/shoe.png', 0.1)
            shoe.center_x = random.randrange(20, SCREEN_WIDTH-20)
            shoe.center_y = random.randrange(20, SCREEN_HEIGHT-20)
            self.shoes.append(shoe)
        for i in range(LEMON_COUNT):
            lemon = arcade.Sprite('images/lemon.png', 0.1)
            lemon.center_x = random.randrange(20, SCREEN_WIDTH-20)
            lemon.center_y = random.randrange(20, SCREEN_HEIGHT-20)
            self.lemons.append(lemon)
        self.physics_engine = arcade.PhysicsEngineSimple(self.felly, self.walls)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.paul, self.walls)
        self.physics_engine3 = arcade.PhysicsEngineSimple(self.baddybadguy, self.walls)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        self.felly.draw()
        self.shoes.draw()
        self.lemons.draw()
        self.walls.draw()
        self.baddies.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if self.counter > 0:
            self.felly_speed = MOVEMENT_SPEED * self.multiplier
            self.baddy_speed = BADDY_SPEED * self.multiplier
            self.counter -= 1
        else:
            self.felly_speed = MOVEMENT_SPEED
            self.baddy_speed = BADDY_SPEED
            self.multiplier = 1
        self.check_for_win()
        self.check_for_catches()
        self.check_for_death()
        self.check_baddy_collision()
        self.shoes.update()
        self.move_baddy(self.paul)
        self.move_baddy(self.baddybadguy)
        self.physics_engine.update()
        self.physics_engine2.update()
        self.physics_engine3.update()

    def check_for_win(self):
        if self.score == SHOE_COUNT:
            nailed_it = NailedIt()
            self.window.show_view(nailed_it)

    def get_acceptable_coordinates(self):
        need_new_coordinates = True
        while need_new_coordinates:
            new_x = random.randrange(20, SCREEN_WIDTH-20)
            new_y = random.randrange(20, SCREEN_HEIGHT-20)
            if max(self.felly.center_x, new_x) - min(self.felly.center_x, new_x) > 100 and  max(self.felly.center_y, new_y) - min(self.felly.center_y, new_y) > 100:
                need_new_coordinates = False

        return new_x, new_y

    def check_baddy_collision(self):
        baddy_collision = arcade.check_for_collision(self.baddybadguy, self.paul)
        if baddy_collision:
            self.baddybadguy.center_x, self.baddybadguy.center_y = self.get_acceptable_coordinates()

    def check_for_catches(self):
        collisions = arcade.check_for_collision_with_list(self.felly, self.shoes)
        for collision in collisions:
            self.score += 1
            collision.kill()
        lemon_collisions = arcade.check_for_collision_with_list(self.felly, self.lemons)
        for lemon_collision in lemon_collisions:
            self.lemon_count -= 1
            print(self.lemon_count)
            lemon_collision.kill()
            if self.lemon_count == 0:
                print("Killing bum")
                self.baddybadguy.kill()

    def check_for_death(self):
        dead_collision = arcade.check_for_collision_with_list(self.felly, self.baddies)
        if dead_collision:
            failed_it = FailedIt()
            self.window.show_view(failed_it)

    def move_baddy(self, baddy):
        felly_coords = self.felly.position
        baddy_coords = baddy.position
        diff_x = felly_coords[0] - baddy_coords[0]
        diff_y = felly_coords[1] - baddy_coords[1]
        if diff_y == 0:
            baddy.change_x = 0
        elif diff_x > 0:
            baddy.change_x = min((math.fabs(diff_x) / math.fabs(diff_y)), self.baddy_speed)
        else:
            baddy.change_x = -1 * min((math.fabs(diff_x) / math.fabs(diff_y)), self.baddy_speed)
        if diff_x == 0:
            baddy.change_y = 0
        elif diff_y > 0:
            baddy.change_y = min((math.fabs(diff_y) / math.fabs(diff_x)), self.baddy_speed)
        else:
            baddy.change_y = -1 * min((math.fabs(diff_y) / math.fabs(diff_x)), self.baddy_speed)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.felly.change_y = self.felly_speed
        elif key == arcade.key.DOWN:
            self.felly.change_y = -self.felly_speed
        elif key == arcade.key.LEFT:
            self.felly.change_x = -self.felly_speed
        elif key == arcade.key.RIGHT:
            self.felly.change_x = self.felly_speed
        elif key == arcade.key.SPACE:
            self.counter = 100
            self.multiplier = 2
            self.felly.change_x *= self.multiplier
            self.felly.change_y *= self.multiplier

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

