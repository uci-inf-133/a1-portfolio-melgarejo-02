import time
from graphics import Canvas

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 800
BALL_SIZE = 30
PADDLE_HEIGHT = 20
PADDLE_WIDTH = 70
PADDLE_SPEED = 20

DELAY = 0.015
SPEED = 5

game_running = False

def hits_bottom(canvas, r):
    top_y = canvas.get_top_y(r)
    return top_y > CANVAS_HEIGHT - BALL_SIZE

def hits_right(canvas, r):
    left_x = canvas.get_left_x(r)
    return left_x > CANVAS_WIDTH - BALL_SIZE

def hits_left(canvas, r):
    left_x = canvas.get_left_x(r)
    return left_x <= 0

def hits_top(canvas, r):
    top_y = canvas.get_top_y(r)
    return top_y <= 0

def check_collision(canvas, ball, paddle) -> bool:
    ball_coords = canvas.bbox(ball)
    paddle_coords = canvas.bbox(paddle)
    return (ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2] and
            ball_coords[3] >= paddle_coords[1] and ball_coords[1] <= paddle_coords[3])

def create_ball(canvas, x, y):
    return canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, color='black')

def create_paddle(canvas):
    return canvas.create_rectangle(
        (CANVAS_WIDTH - PADDLE_WIDTH) // 2, CANVAS_HEIGHT - PADDLE_HEIGHT,
        (CANVAS_WIDTH + PADDLE_WIDTH) // 2, CANVAS_HEIGHT,
        color='black'
    )

def move_ball(canvas, ball, dx, dy):
    canvas.move(ball, dx, dy)

def move(event, canvas, paddle):
    if event.keysym == "Left" and canvas.bbox(paddle)[0] > 0:
        canvas.move(paddle, -PADDLE_SPEED, 0)
    elif event.keysym == "Right" and canvas.bbox(paddle)[0] < CANVAS_WIDTH - PADDLE_WIDTH:
        canvas.move(paddle, PADDLE_SPEED, 0)

def toggle_game(event):
    global game_running
    game_running = not game_running  # Switch between paused and running

def game_over():
    print("You lose!")
    exit()

def main():
    global game_running

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Move BALL')
    canvas.set_canvas_background_color('white')

    ball = canvas.create_oval(10, 10, BALL_SIZE, BALL_SIZE, color='black')
    paddle = create_paddle(canvas)
    x_speed = y_speed = 1

    canvas.bind("<space>", toggle_game)
    canvas.bind("<KeyPress-Left>", lambda event: move(event, canvas, paddle))
    canvas.bind("<KeyPress-Right>", lambda event: move(event, canvas, paddle))
    canvas.focus_set()

    while True:
        if game_running:
            if hits_bottom(canvas, ball):
                game_over()
            if hits_top(canvas, ball):
                y_speed = 1
            if hits_left(canvas, ball):
                x_speed = 1
            if hits_right(canvas, ball):
                x_speed = -1
            if check_collision(canvas, ball, paddle):
                y_speed = -1

            move_ball(canvas, ball, x_speed * SPEED, y_speed * SPEED)

        canvas.update()
        time.sleep(DELAY)

    canvas.mainloop()

if __name__ == "__main__":
    main()
