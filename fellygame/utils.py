import arcade

def create_walls(SCREEN_WIDTH, SCREEN_HEIGHT):
    walls = arcade.SpriteList()
    for i in range(0, SCREEN_WIDTH):
        wall = arcade.Sprite('images/wall.png', 0.1)
        wall.center_y = 0
        wall.center_x = i
        walls.append(wall)
    for i in range(0, SCREEN_WIDTH):
        wall = arcade.Sprite('images/wall.png', 0.1)
        wall.center_y = SCREEN_HEIGHT
        wall.center_x = i
        walls.append(wall)
    for i in range(0, SCREEN_HEIGHT):
        wall = arcade.Sprite('images/wall.png', 0.1)
        wall.center_x = 0
        wall.center_y = i
        walls.append(wall)
    for i in range(0, SCREEN_HEIGHT):
        wall = arcade.Sprite('images/wall.png', 0.1)
        wall.center_x = SCREEN_WIDTH
        wall.center_y = i
        walls.append(wall)

    return walls
