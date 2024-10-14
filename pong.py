import py5
import random

# Variables globales
paddle1_y = paddle2_y = 0
paddle_width = 20
paddle_height = 100
paddle_speed = ball_size = 20
ball_x = ball_y = ball_dx = ball_dy = 0
player1_score = player2_score = 0
start_time = 0  # Tiempo de inicio
elapsed_time = 0  # Tiempo transcurrido

# Variables del power-up
power_up_x = power_up_y = 0
power_up_active = False
power_up_timer = 0
power_up_duration = 5000  # Duración del power-up en milisegundos

# Estado de las teclas presionadas
keys = set()

def setup():
    py5.size(800, 400)
    global start_time
    reset_game()
    start_time = py5.millis()  # Guardar el tiempo de inicio

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score, power_up_active, paddle_height
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5
    ball_dy = 3
    paddle1_y = py5.height / 2 - paddle_height / 2
    paddle2_y = py5.height / 2 - paddle_height / 2
    player1_score = 0
    player2_score = 0
    power_up_active = False  # Reiniciar el estado del power-up
    paddle_height = 100  # Reiniciar altura del paddle

def draw():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score, elapsed_time
    global power_up_active, power_up_x, power_up_y, power_up_timer, paddle_height

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

    # Dibujar ayuda de teclas
    py5.text_size(16)
    py5.text_align(py5.LEFT)
    py5.fill(255)
    py5.text("Jugador 1: W (Arriba), S (Abajo)", 10, 30)
    py5.text_align(py5.RIGHT)
    py5.text("Jugador 2: O (Arriba), L (Abajo)", py5.width - 10, 30)

    # Calcular y mostrar el tiempo transcurrido
    elapsed_time = int((py5.millis() - start_time) / 1000)  # Convertir a segundos
    py5.text_size(24)
    py5.fill(255)
    py5.text(f"Tiempo: {elapsed_time} s", py5.width / 2, 80)

    # Mostrar el power-up
    if power_up_active:
        py5.fill(255, 204, 0)
        py5.ellipse(power_up_x, power_up_y, 20, 20)
        # Verificar el tiempo del power-up
        if py5.millis() - power_up_timer > power_up_duration:
            power_up_active = False  # Desactivar el power-up

    # Generar el power-up si no está activo
    if not power_up_active and random.random() < 0.01:  # 1% de probabilidad de aparecer
        power_up_x = random.randint(100, py5.width - 100)
        power_up_y = random.randint(50, py5.height - 50)
        power_up_active = True
        power_up_timer = py5.millis()  # Reiniciar el temporizador

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

    # Verificar colisión con el power-up
    if power_up_active:
        if (power_up_x - 10 <= 30 + paddle_width <= power_up_x + 10 and
            paddle1_y < power_up_y < paddle1_y + paddle_height):
            paddle_height += 50  # Aumentar la altura del paddle del jugador 1
            power_up_active = False

        if (power_up_x - 10 <= py5.width - 30 - paddle_width <= power_up_x + 10 and
            paddle2_y < power_up_y < paddle2_y + paddle_height):
            paddle_height += 50  # Aumentar la altura del paddle del jugador 2
            power_up_active = False

def key_pressed():
    global keys
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
