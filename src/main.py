from pyray import *
from random import randint

apples = []
apple_timer = 0
apple_frequency = 25
snake_parts = []
snake_head = Rectangle(240, 240, 10, 10)
snake_direction = Vector2(0, 0)
snake_speed = 10


class Snake_part:
    def __init__(self, part=Rectangle, last_pos=Vector2):
        self.part = part
        self.last_pos = last_pos


def draw_grid2D(xline, yline, spacing, rectangle: Rectangle, color):
    for x in range(xline):
        draw_line(
            x * spacing, int(rectangle.y), x * spacing, int(rectangle.height), color
        )
        for y in range(yline):
            draw_line(
                int(rectangle.x), y * spacing, int(rectangle.width), y * spacing, color
            )
    draw_rectangle_lines_ex(rectangle, 1, color)


def randint_ending_in_0(low, high):
    low = (low + 9) // 10 * 10  # Round up to the nearest 10
    high = high // 10 * 10  # Round down to the nearest 10
    return randint(low // 10, high // 10) * 10


def death():
    snake_head.x = 240
    snake_head.y = 240
    snake_direction.x = 0
    snake_direction.y = 0
    snake_parts.clear()


init_window(500, 500, "snake")
init_audio_device()

eat_apple_sound = load_sound("assets/nom-nom-nom_gPJiWn4.mp3")

set_target_fps(10)

while not window_should_close():
    for i in snake_parts:
        if snake_parts.index(i) == 0:
            i.last_pos = Vector2(i.part.x, i.part.y)
            i.part.x = snake_head.x
            i.part.y = snake_head.y
        else:
            i.last_pos = Vector2(i.part.x, i.part.y)
            i.part.x = snake_parts[snake_parts.index(i) - 1].last_pos.x
            i.part.y = snake_parts[snake_parts.index(i) - 1].last_pos.y

    apple = Rectangle(
        randint_ending_in_0(10, 490), randint_ending_in_0(10, 490), 10, 10
    )

    apple_timer += 1

    if apple_timer == apple_frequency:
        apples.append(apple)
        apple_timer = 0
    if is_key_pressed(KEY_W) and snake_direction.y != 1:
        snake_direction.y = -1
        snake_direction.x = 0
    elif is_key_pressed(KEY_S) and snake_direction.y != -1:
        snake_direction.y = 1
        snake_direction.x = 0
    if is_key_pressed(KEY_A) and snake_direction.x != 1:
        snake_direction.x = -1
        snake_direction.y = 0
    elif is_key_pressed(KEY_D) and snake_direction.x != -1:
        snake_direction.x = 1
        snake_direction.y = 0
    if snake_head.x == -10 or snake_head.x == 500:
        death()
    if snake_head.y == -10 or snake_head.y == 500:
        death()

    for i in apples:
        if check_collision_recs(i, snake_head):
            snake_parts.append(Snake_part(Rectangle(-10, -10, 10, 10), Vector2(0, 0)))
            apples.pop(apples.index(i))
            play_sound(eat_apple_sound)
    if is_key_down(KEY_R):
        snake_parts.append(Snake_part(Rectangle(-10, -10, 10, 10), Vector2(0, 0)))

    snake_head.x += snake_speed * snake_direction.x
    snake_head.y += snake_speed * snake_direction.y

    begin_drawing()
    clear_background(BLACK)

    draw_grid2D(100, 100, 10, Rectangle(498, 498, 0, 0), WHITE)

    for i in apples:
        draw_rectangle_rec(i, RED)

    for i in snake_parts:
        draw_rectangle_rec(i.part, GREEN)

    draw_rectangle_rec(snake_head, GREEN)

    end_drawing()
close_window()
