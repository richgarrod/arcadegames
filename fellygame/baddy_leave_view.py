import time
import arcade

class BaddyLeave(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.AMBER)

    def __init__(self, game_view):
        super().__init__()
        self.success_text = "Baddy Leaving, No Lemons, No Point!"
        self.game_view = game_view

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.success_text, 50, 200, arcade.color.RED, 25)

    def on_key_press(self, key, modifiers):
        time.sleep(1)
        self.window.show_view(self.game_view)

