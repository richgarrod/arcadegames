import arcade

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
