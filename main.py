import turtle
import math
import random

# Screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Space Invaders")
screen.setup(width=800, height=600)

# Predefined shapes (no need to register since they are built-in)
player_shape = "triangle"
enemy_shape = "square"
projectile_shape = "triangle"

# Player
player = turtle.Turtle()
player.color("blue")
player.shape(player_shape)
player.penup()
player.speed(0)
player.goto(0, -250)
player.setheading(90)

# Player movement
player_speed = 15


def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -370:
        x = -370
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 370:
        x = 370
    player.setx(x)


# Enemies
num_of_enemies = 5
enemies = []

for _ in range(num_of_enemies):
    enemy = turtle.Turtle()
    enemy.color("red")
    enemy.shape(enemy_shape)
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-300, 300)
    y = random.randint(100, 250)
    enemy.goto(x, y)
    enemies.append(enemy)

enemy_speed = 2

# Projectile
projectile = turtle.Turtle()
projectile.color("yellow")
projectile.shape(projectile_shape)
projectile.penup()
projectile.speed(0)
projectile.goto(0, -400)
projectile.setheading(90)
projectile.hideturtle()

projectile_speed = 20
projectile_state = "ready"  # "ready" or "fired"


def fire_projectile():
    global projectile_state
    if projectile_state == "ready":
        projectile_state = "fired"
        x = player.xcor()
        y = player.ycor() + 10
        projectile.goto(x, y)
        projectile.showturtle()


# Collision detection
def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    return distance < 20


# Keyboard bindings
screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(fire_projectile, "space")

# Game loop
score = 0
lives = 3

score_display = turtle.Turtle()
score_display.color("white")
score_display.hideturtle()
score_display.penup()
score_display.goto(-350, 260)
score_display.write(f"Score: {score}  Lives: {lives}", align="left", font=("Arial", 16, "normal"))

game_over = False

while not game_over:
    screen.update()

    # Move enemies
    for enemy in enemies:
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Change direction and move down
        if x > 370 or x < -370:
            enemy_speed *= -1
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)

        # Check for collision with player
        if is_collision(enemy, player):
            lives -= 1
            score_display.clear()
            score_display.write(f"Score: {score}  Lives: {lives}", align="left", font=("Arial", 16, "normal"))
            enemy.goto(random.randint(-300, 300), random.randint(100, 250))
            if lives == 0:
                score_display.clear()
                score_display.write("GAME OVER", align="center", font=("Arial", 24, "normal"))
                game_over = True

        # Check for collision with projectile
        if is_collision(projectile, enemy):
            score += 10
            score_display.clear()
            score_display.write(f"Score: {score}  Lives: {lives}", align="left", font=("Arial", 16, "normal"))
            enemy.goto(random.randint(-300, 300), random.randint(100, 250))
            projectile.hideturtle()
            projectile_state = "ready"

    # Move projectile
    if projectile_state == "fired":
        y = projectile.ycor()
        y += projectile_speed
        projectile.sety(y)

        if y > 280:
            projectile.hideturtle()
            projectile_state = "ready"

screen.mainloop()
