from graphics import Canvas
import random
import time

# Canvas dimensions

CANVAS_WIDTH = 350
CANVAS_HEIGHT = 400

# Paddle settings

PADDLE_LENGTH = 80
PADDLE_THICKNESS = 10
PADDLE_EDGE_DIST = 20
COMP_PADDLE_COLOR = "#B00020"
USER_PADDLE_COLOR = "#0052CC"
PADDLE_SPEED = 8

DIFFICULTY_SETTINGS = {
    "1": {"name": "Easy",   "comp_speed": 1.5},
    "2": {"name": "Medium", "comp_speed": 3.0},
    "3": {"name": "Hard",   "comp_speed": 5.0},
}

# Ball settings

BALL_DIAMETER = 10
BALL_RADIUS = BALL_DIAMETER / 2
INITIAL_BALL_SPEED = 4
BALL_SPEED_INCREMENT = 0.2
MAX_BALL_SPEED = 8

# Scoring

WINNING_SCORE = 5

# Typography

GAME_TITLE = "Tennis Showdown"
TITLE_FONT = "Magneto"
FONT = "Arial Black"
FRAME_DELAY = 1 / 60

# Game-state constants

STATE_TITLE = "TITLE"
STATE_COLOR_CHOICE = "COLOR_CHOICE"
STATE_DIFFICULTY = "DIFFICULTY"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"

STATE_USER_SCORED = "USER_SCORED"
STATE_COMP_SCORED = "COMP_SCORED"

GAME_OVER_TEXT_COLOR = "#111111"

# Screen helpers

def show_titlecard(canvas):
    objs = []
    objs.append(canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "#C0FFEE"))
    objs.append(canvas.create_text(
        CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 15,
        GAME_TITLE, TITLE_FONT, 30, "#2E2E2E", anchor="center"
    ))
    objs.append(canvas.create_text(
        CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 60,
        "Press Enter to start", "Lucida Console", 20, "#2E2E2E", anchor="center"
    ))

    # Tennis icon
    icon_h = CANVAS_HEIGHT / 2
    icon_w = int(icon_h * (456 / 547))
    icon_top_y = CANVAS_HEIGHT / 2
    icon_left_x = (CANVAS_WIDTH - icon_w) / 2
    objs.append(canvas.create_image_with_size(
        icon_left_x, icon_top_y, icon_w, int(icon_h), "tennis icon.png"
    ))

    # Wait for input
    result = False
    waiting = True
    while waiting:
        for key in canvas.get_new_key_presses():
            if key == "Enter":
                result = True
                waiting = False
            elif key == "Escape":
                waiting = False
        time.sleep(FRAME_DELAY)

    for obj in objs:
        canvas.delete(obj)
    return result


def choose_bg_color(canvas):
    color_options = {
        "1": {"name": "Blue",  "value": "#A7C7E7"},
        "2": {"name": "Green", "value": "#77DD77"},
        "3": {"name": "Pink",  "value": "#FFD1DC"},
        "4": {"name": "Grey",  "value": "#CFCFC4"},
        "5": {"name": "Aqua",  "value": "#D8F3E9"},
    }

    objs = []
    objs.append(canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "black"))

    header_y = CANVAS_HEIGHT * 0.25
    objs.append(canvas.create_text(
        CANVAS_WIDTH / 2, header_y,
        "Choose Table Color", FONT, 26, "white", anchor="center"
    ))

    current_y = header_y + 26 + 30
    for key, option in color_options.items():
        objs.append(canvas.create_text(
            CANVAS_WIDTH / 2, current_y,
            f"{key}. {option['name']}", FONT, 20, option["value"], anchor="center"
        ))
        current_y += 30

    error_obj = None
    while True:
        for key in canvas.get_new_key_presses():
            if key in color_options:
                if error_obj:
                    canvas.delete(error_obj)
                for obj in objs:
                    canvas.delete(obj)
                return color_options[key]["value"]
            else:
                if error_obj:
                    canvas.delete(error_obj)
                error_obj = canvas.create_text(
                    CANVAS_WIDTH / 2, 320,
                    "Invalid choice. Press a key between 1 and 5.",
                    "Lucida Console", 12, "#FF0000", anchor="center"
                )
        time.sleep(FRAME_DELAY)


def choose_difficulty(canvas):
    objs = []
    objs.append(canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "black"))

    header_y = CANVAS_HEIGHT * 0.25
    objs.append(canvas.create_text(
        CANVAS_WIDTH / 2, header_y,
        "Choose Difficulty", FONT, 26, "white", anchor="center"
    ))

    difficulty_colors = {"1": "#77DD77", "2": "#FFD700", "3": "#FF6B6B"}
    current_y = header_y + 26 + 30
    for key, setting in DIFFICULTY_SETTINGS.items():
        objs.append(canvas.create_text(
            CANVAS_WIDTH / 2, current_y,
            f"{key}. {setting['name']}", FONT, 20,
            difficulty_colors[key], anchor="center"
        ))
        current_y += 30

    error_obj = None
    while True:
        for key in canvas.get_new_key_presses():
            if key in DIFFICULTY_SETTINGS:
                if error_obj:
                    canvas.delete(error_obj)
                for obj in objs:
                    canvas.delete(obj)
                return DIFFICULTY_SETTINGS[key]["comp_speed"]
            else:
                if error_obj:
                    canvas.delete(error_obj)
                error_obj = canvas.create_text(
                    CANVAS_WIDTH / 2, 320,
                    "Invalid choice. Press a key between 1 and 3.",
                    "Lucida Console", 12, "#FF0000", anchor="center"
                )
        time.sleep(FRAME_DELAY)


def show_gameover(canvas, winner_text, user_score, comp_score):

    canvas.clear()
    objs = []

    bg_color = "#0A7FF6" if winner_text == "You Win! 🎉" else "#97C90F"
    objs.append(canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, bg_color))

    objs.append(canvas.create_text(
        CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 110,
        winner_text, FONT, 30, GAME_OVER_TEXT_COLOR, anchor="center"
    ))

    score_str = f"Final Score:  You {user_score} – {comp_score} Computer"
    objs.append(canvas.create_text(
        CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 75,
        score_str, FONT, 13, GAME_OVER_TEXT_COLOR, anchor="center"
    ))

    if winner_text == "You Win! 🎉":
        img_file = "trophy.png"
        img_w = img_h = 150
    else:
        img_file = "sad.png"
        img_h = 150
        img_w = int(img_h * (502 / 497))

    objs.append(canvas.create_image_with_size(
        (CANVAS_WIDTH - img_w) / 2,
        (CANVAS_HEIGHT - img_h) / 2,
        img_w, img_h, img_file
    ))

    objs.append(canvas.create_text(
        CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 110,
        "Press Enter to Restart  or  Esc to Quit",
        FONT, 13, GAME_OVER_TEXT_COLOR, anchor="center"
    ))

    return objs

# Game-object creators

def create_comp_paddle(canvas):
    """Create and return the computer's paddle (top, red)."""
    left_x = (CANVAS_WIDTH / 2) - (PADDLE_LENGTH / 2)
    top_y = PADDLE_EDGE_DIST
    return canvas.create_rectangle(
        left_x, top_y,
        left_x + PADDLE_LENGTH, top_y + PADDLE_THICKNESS,
        COMP_PADDLE_COLOR, "black"
    )


def create_user_paddle(canvas):
    """Create and return the player's paddle (bottom, blue)."""
    left_x = (CANVAS_WIDTH / 2) - (PADDLE_LENGTH / 2)
    top_y = CANVAS_HEIGHT - PADDLE_EDGE_DIST - PADDLE_THICKNESS
    return canvas.create_rectangle(
        left_x, top_y,
        left_x + PADDLE_LENGTH, top_y + PADDLE_THICKNESS,
        USER_PADDLE_COLOR, "black"
    )


def create_ball(canvas):
    start_x = CANVAS_WIDTH / 2 - BALL_RADIUS
    start_y = CANVAS_HEIGHT / 2 - BALL_RADIUS
    ball = canvas.create_oval(
        start_x, start_y,
        start_x + BALL_DIAMETER, start_y + BALL_DIAMETER,
        "#FFA500", "black"
    )
    dy = INITIAL_BALL_SPEED * (1 if random.random() >= 0.5 else -1)
    dx = random.uniform(INITIAL_BALL_SPEED * 0.3, INITIAL_BALL_SPEED * 0.8)
    dx *= (1 if random.random() >= 0.5 else -1)
    return ball, dx, dy


def reset_ball(canvas, ball, serve_dy_sign):
    canvas.moveto(
        ball,
        CANVAS_WIDTH / 2 - BALL_RADIUS,
        CANVAS_HEIGHT / 2 - BALL_RADIUS
    )
    dy = INITIAL_BALL_SPEED * serve_dy_sign
    dx = random.uniform(INITIAL_BALL_SPEED * 0.3, INITIAL_BALL_SPEED * 0.8)
    dx *= (1 if random.random() >= 0.5 else -1)
    return dx, dy

# Game setup

def setup_game(canvas, bg_color):
    canvas.clear()

    # Background
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, bg_color)

    # Centre line
    canvas.create_line(0, CANVAS_HEIGHT / 2, CANVAS_WIDTH, CANVAS_HEIGHT / 2, "white")

    # Score display
    comp_score_text = canvas.create_text(
        CANVAS_WIDTH - 30, CANVAS_HEIGHT / 2 - 24,
        "0", FONT, 24, COMP_PADDLE_COLOR
    )
    user_score_text = canvas.create_text(
        CANVAS_WIDTH - 30, CANVAS_HEIGHT / 2 + 3,
        "0", FONT, 24, USER_PADDLE_COLOR
    )

    comp_paddle = create_comp_paddle(canvas)
    user_paddle = create_user_paddle(canvas)
    ball, ball_dx, ball_dy = create_ball(canvas)

    return {
        "user_score": 0,
        "comp_score": 0,
        "comp_score_text": comp_score_text,
        "user_score_text": user_score_text,
        "comp_paddle": comp_paddle,
        "user_paddle": user_paddle,
        "ball": ball,
        "ball_dx": ball_dx,
        "ball_dy": ball_dy,
    }

# Per-frame update functions

def move_user_paddle(canvas, paddle, keys):
    """Slide the player's paddle left/right based on arrow-key input."""
    if not paddle:
        return
    current_x = canvas.get_left_x(paddle)
    for key in keys:
        if key == "ArrowLeft":
            dx = max(-PADDLE_SPEED, -current_x)
            canvas.move(paddle, dx, 0)
        elif key == "ArrowRight":
            dx = min(PADDLE_SPEED, CANVAS_WIDTH - (current_x + PADDLE_LENGTH))
            canvas.move(paddle, dx, 0)


def move_comp_paddle(canvas, paddle, ball, ball_dy, comp_speed):
    if not paddle or not ball:
        return
    # Only track the ball when it is heading toward the computer's side
    if ball_dy > 0:
        return

    paddle_center_x = canvas.get_left_x(paddle) + PADDLE_LENGTH / 2
    ball_center_x = canvas.get_left_x(ball) + BALL_RADIUS

    diff = ball_center_x - paddle_center_x
    if abs(diff) <= 1:
        return

    move_dx = max(-comp_speed, min(comp_speed, diff))

    # Clamp to canvas boundaries
    current_x = canvas.get_left_x(paddle)
    if current_x + move_dx < 0:
        move_dx = -current_x
    elif current_x + PADDLE_LENGTH + move_dx > CANVAS_WIDTH:
        move_dx = CANVAS_WIDTH - (current_x + PADDLE_LENGTH)

    if move_dx != 0:
        canvas.move(paddle, move_dx, 0)


def _deflect_dx(current_dx, ball_center_x, paddle_left_x):
    """Return a new dx after a paddle collision, factoring in impact offset."""
    impact_offset = (ball_center_x - (paddle_left_x + PADDLE_LENGTH / 2)) / (PADDLE_LENGTH / 2)
    new_dx = current_dx + impact_offset * (INITIAL_BALL_SPEED * 0.5)
    max_dx = INITIAL_BALL_SPEED * 1.5
    new_dx = max(-max_dx, min(max_dx, new_dx))
    # Ensure a minimum horizontal component so the ball never travels vertically
    min_dx = INITIAL_BALL_SPEED * 0.2
    if abs(new_dx) < min_dx:
        new_dx = min_dx * (1 if new_dx >= 0 else -1)
    return new_dx


def update_ball(canvas, ball, dx, dy, comp_paddle, user_paddle):
    canvas.move(ball, dx, dy)

    left_x = canvas.get_left_x(ball)
    top_y = canvas.get_top_y(ball)
    right_x = left_x + BALL_DIAMETER
    bottom_y = top_y + BALL_DIAMETER
    center_x = left_x + BALL_RADIUS

    # Scoring
    if top_y < 0:
        return dx, dy, STATE_USER_SCORED
    if bottom_y > CANVAS_HEIGHT:
        return dx, dy, STATE_COMP_SCORED

    new_dx, new_dy = dx, dy

    # Side-wall bouncing
    if left_x <= 0:
        new_dx = abs(dx)
        canvas.moveto(ball, 0.1, top_y)
    elif right_x >= CANVAS_WIDTH:
        new_dx = -abs(dx)
        canvas.moveto(ball, CANVAS_WIDTH - BALL_DIAMETER - 0.1, top_y)

    # Computer paddle collision
    if dy < 0 and top_y <= PADDLE_EDGE_DIST + PADDLE_THICKNESS + BALL_DIAMETER:
        if comp_paddle:
            coords = canvas.coords(comp_paddle)
            cp_left, cp_top, *_ = coords
            cp_right = cp_left + PADDLE_LENGTH
            cp_bottom = cp_top + PADDLE_THICKNESS

            if right_x > cp_left and left_x < cp_right and bottom_y > cp_top and top_y < cp_bottom:
                new_dy = min(abs(dy) + BALL_SPEED_INCREMENT, MAX_BALL_SPEED)
                new_dx = _deflect_dx(new_dx, center_x, cp_left)
                canvas.moveto(ball, left_x, cp_bottom + 0.1)

    # User paddle collision
    if dy > 0 and bottom_y >= CANVAS_HEIGHT - PADDLE_EDGE_DIST - PADDLE_THICKNESS - BALL_DIAMETER:
        if user_paddle:
            coords = canvas.coords(user_paddle)
            up_left, up_top, *_ = coords
            up_right = up_left + PADDLE_LENGTH
            up_bottom = up_top + PADDLE_THICKNESS

            if right_x > up_left and left_x < up_right and top_y < up_bottom and bottom_y > up_top:
                new_dy = -min(abs(dy) + BALL_SPEED_INCREMENT, MAX_BALL_SPEED)
                new_dx = _deflect_dx(new_dx, center_x, up_left)
                canvas.moveto(ball, left_x, up_top - BALL_DIAMETER - 0.1)

    return new_dx, new_dy, STATE_PLAYING

# Main game loop

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    game_state = STATE_TITLE
    game_data = {}
    game_over_objs = []
    flash_objs = []
    bg_color = "#A7C7E7"
    comp_speed = DIFFICULTY_SETTINGS["2"]["comp_speed"]

    while True:
        key_press = canvas.get_new_key_presses()

        if game_state == STATE_TITLE:
            if not show_titlecard(canvas):
                print("Exiting...")
                return
            canvas.clear()
            game_state = STATE_COLOR_CHOICE

        elif game_state == STATE_COLOR_CHOICE:
            bg_color = choose_bg_color(canvas)
            game_state = STATE_DIFFICULTY

        elif game_state == STATE_DIFFICULTY:
            comp_speed = choose_difficulty(canvas)
            game_data = setup_game(canvas, bg_color)
            game_state = STATE_PLAYING

        elif game_state == STATE_PLAYING:
            move_user_paddle(canvas, game_data["user_paddle"], key_press)
            move_comp_paddle(
                canvas, game_data["comp_paddle"],
                game_data["ball"], game_data["ball_dy"],
                comp_speed
            )

            new_dx, new_dy, round_state = update_ball(
                canvas,
                game_data["ball"],
                game_data["ball_dx"],
                game_data["ball_dy"],
                game_data["comp_paddle"],
                game_data["user_paddle"],
            )
            game_data["ball_dx"] = new_dx
            game_data["ball_dy"] = new_dy

            if round_state == STATE_USER_SCORED:
                game_data["user_score"] += 1
                canvas.change_text(game_data["user_score_text"], str(game_data["user_score"]))
                flash_objs.append(canvas.create_text(
                    CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 14,
                    "You Scored!", FONT, 24, USER_PADDLE_COLOR, anchor="center"
                ))
                if game_data["user_score"] >= WINNING_SCORE:
                    game_state = STATE_GAME_OVER
                    game_over_objs = show_gameover(
                        canvas, "You Win! 🎉",
                        game_data["user_score"], game_data["comp_score"]
                    )
                else:
                    time.sleep(1)
                    for obj in flash_objs:
                        canvas.delete(obj)
                    flash_objs = []
                    game_data["ball_dx"], game_data["ball_dy"] = reset_ball(
                        canvas, game_data["ball"], 1
                    )

            elif round_state == STATE_COMP_SCORED:
                game_data["comp_score"] += 1
                canvas.change_text(game_data["comp_score_text"], str(game_data["comp_score"]))
                flash_objs.append(canvas.create_text(
                    CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 14,
                    "Computer Scored!", FONT, 24, COMP_PADDLE_COLOR, anchor="center"
                ))
                if game_data["comp_score"] >= WINNING_SCORE:
                    game_state = STATE_GAME_OVER
                    game_over_objs = show_gameover(
                        canvas, "You Lose! ☹️",
                        game_data["user_score"], game_data["comp_score"]
                    )
                else:
                    time.sleep(1)
                    for obj in flash_objs:
                        canvas.delete(obj)
                    flash_objs = []
                    game_data["ball_dx"], game_data["ball_dy"] = reset_ball(
                        canvas, game_data["ball"], -1
                    )

        elif game_state == STATE_GAME_OVER:
            for key in key_press:
                if key == "Escape":
                    print("Exiting...")
                    return
                elif key == "Enter":
                    for obj in game_over_objs:
                        canvas.delete(obj)
                    game_over_objs = []
                    game_data = setup_game(canvas, bg_color)
                    game_state = STATE_PLAYING
                    break

        time.sleep(FRAME_DELAY)


if __name__ == "__main__":
    main()
