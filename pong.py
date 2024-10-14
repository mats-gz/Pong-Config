import py5

# Variables globales
paddle1_y = paddle2_y = 0
paddle_width = paddle_height = 0
paddle_speed = ball_size = 0
ball_x = ball_y = ball_dx = ball_dy = 0
player1_score = player2_score = 0
login_successful = False

# Estado de las teclas presionadas
keys = set()

# Variables para el login
player1_name = ""
player2_name = ""
input_text = ""
current_input = "player1"  # Controla si está escribiendo el nombre del jugador 1 o jugador 2

def setup():
    py5.size(800, 400)
    global paddle_width, paddle_height, paddle_speed, ball_size
    global ball_x, ball_y, ball_dx, ball_dy
    global paddle1_y, paddle2_y, player1_score, player2_score
    paddle_width = 20
    paddle_height = 100
    paddle_speed = 7
    ball_size = 20
    reset_game()


def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5
    ball_dy = 3
    paddle1_y = py5.height / 2 - paddle_height / 2
    paddle2_y = py5.height / 2 - paddle_height / 2
    player1_score = 0
    player2_score = 0


def draw():
    global login_successful

    py5.background(0)

    if not login_successful:
        show_login_screen()
    else:
        play_game()


def show_login_screen():
    global input_text, player1_name, player2_name, current_input

    py5.fill(255)
    py5.text_size(32)
    py5.text_align(py5.CENTER)

    py5.text("Ingresar Nombres", py5.width / 2, py5.height / 3)
    
    py5.text_size(20)
    py5.text_align(py5.LEFT)
    py5.text(f"Jugador 1: {player1_name}", py5.width / 4, py5.height / 2)
    py5.text(f"Jugador 2: {player2_name}", py5.width / 4, py5.height / 2 + 30)
    
    py5.text_size(16)
    py5.text(f"Escribiendo: {input_text}", py5.width / 4, py5.height / 2 + 60)

    if current_input == "player1":
        py5.text("Presiona Enter para confirmar Jugador 1", py5.width / 4, py5.height / 2 + 90)
    else:
        py5.text("Presiona Enter para confirmar Jugador 2", py5.width / 4, py5.height / 2 + 90)


def play_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score

    py5.background(0)

    # Dibujar los paddles
    py5.rect(30, paddle1_y, paddle_width, paddle_height)  # Pala izquierda
    py5.rect(py5.width - 30 - paddle_width, paddle2_y, paddle_width, paddle_height)  # Pala derecha

    # Dibujar la pelota
    py5.ellipse(ball_x, ball_y, ball_size, ball_size)

    # Dibujar el marcador
    py5.text_size(32)
    py5.text_align(py5.CENTER)
    py5.fill(255)
    py5.text(f"{player1_score} - {player2_score}", py5.width / 2, 40)

    # Actualizar posición de la pelota
    ball_x += ball_dx
    ball_y += ball_dy

    # Rebote de la pelota en la parte superior e inferior
    if ball_y <= ball_size / 2 or ball_y >= py5.height - ball_size / 2:
        ball_dy *= -1

    # Verificar colisiones con los paddles
    if ball_x - ball_size / 2 <= 30 + paddle_width:
        if paddle1_y < ball_y < paddle1_y + paddle_height:
            ball_dx *= -1
            ball_x = 30 + paddle_width + ball_size / 2

    if ball_x + ball_size / 2 >= py5.width - 30 - paddle_width:
        if paddle2_y < ball_y < paddle2_y + paddle_height:
            ball_dx *= -1
            ball_x = py5.width - 30 - paddle_width - ball_size / 2

    # Si la pelota sale por la izquierda
    if ball_x < 0:
        player2_score += 1
        reset_ball()

    # Si la pelota sale por la derecha
    if ball_x > py5.width:
        player1_score += 1
        reset_ball()

    # Limitar el movimiento de los paddles
    if 'w' in keys and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if 's' in keys and paddle1_y < py5.height - paddle_height:
        paddle1_y += paddle_speed
    if 'o' in keys and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if 'l' in keys and paddle2_y < py5.height - paddle_height:
        paddle2_y += paddle_speed


def key_pressed():
    global input_text, player1_name, player2_name, login_successful, current_input

    # Si no ha hecho login, gestionar la entrada de los nombres de los jugadores
    if not login_successful:
        if py5.key == py5.ENTER:
            if current_input == "player1":
                player1_name = input_text
                input_text = ""
                current_input = "player2"
            elif current_input == "player2":
                player2_name = input_text
                input_text = ""
                login_successful = True  # Ambos nombres ingresados, comienza el juego
        elif py5.key == py5.BACKSPACE:
            input_text = input_text[:-1]  # Borrar el último carácter
        else:
            input_text += py5.key  # Añadir la tecla presionada al texto
    else:
        keys.add(py5.key)


def key_released():
    global keys
    keys.discard(py5.key)


def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx *= -1
    ball_dy = py5.random(-3, 3)


if __name__ == "__main__":
    py5.run_sketch()
