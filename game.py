import turtle
import os
import math
import random
import winsound
import pygame
from pygame import mixer
pygame.init()

# set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)

# register the shapes
wn.register_shape("invader.gif")
wn.register_shape("player.gif")


# draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# set the score to 0
score = 0

# draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()


# create a player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

player.speed = 0



# choose a number of enemies
number_of_enemies = 30
# create an empty list of enemies
enemies = []

# add enemies to the list
for i in range(number_of_enemies):
    # create the enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0


for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setposition(x, y)
    # update the enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.1

# create the player bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 5

# define bullet state
# ready - ready to fire
# fire - bullet is fire
bulletstate = "ready"

# move the player left and right
def move_left():
    player.speed = -2


def move_right():
    player.speed = 2

def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    # declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate =="ready":
        winsound.PlaySound("laser", winsound.SND_ASYNC)
        bulletstate = "fire"
        # move the bullet to the just above player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(), 2)+math.pow(t1.ycor()-t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# create keyboard binding
wn.listen()
wn.onkeypress(move_left, "a")
wn.onkeypress(move_right, "d")
wn.onkeypress(fire_bullet, "space")

#play background music
# winsound.PlaySound("bgm", winsound.SND_ASYNC)
mixer.music.load("bgm.wav")
mixer.music.play(-1)

# main game loop
while True:
    wn.update()
    move_player()

    for enemy in enemies:
        # move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # move the enemy back and down
        if enemy.xcor() > 280:
            # move all the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                # change enemy direction
            enemyspeed *= -1

        if enemy.xcor() < -280:
            # move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change enemy direction
            enemyspeed *= -1

            # check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            winsound.PlaySound("explosion", winsound.SND_ASYNC)
            # reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            # reset the enemy
            enemy.setposition(0, 10000)
            # update score
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("Game over")
            break
    # move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
    if score == 300:
        victorie_pen = turtle.Turtle()
        victorie_pen.speed(0)
        victorie_pen.color("white")
        victorie_pen.penup()
        victorie_pen.setposition(-200, 0)
        scorestring = "YOU WIN"
        victorie_pen.write(scorestring, False, align="left", font=("Arial", 30, "normal"))
        victorie_pen.hideturtle()


turtle.delay(1)
turtle.done()
wn.mainloop()
