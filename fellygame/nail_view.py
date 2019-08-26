import arcade

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
