import os
import turtle
import random
import math
import winsound
import time

#turtle.register_shape("l45.gif")
#turtle.register_shape("firebal.gif")
wn = turtle.Screen()
wn.bgcolor("lightblue")
wn.title("spele")
#wn.bgpic("bce.gif")
ropen = turtle.Turtle()
ropen.speed(0)
ropen.color("black")
ropen.penup()
ropen.setposition(-384,-216)
ropen.pendown()
ropen.pensize(4)
ropen.fd(768)
ropen.lt(90)
ropen.fd(432)
ropen.lt(90)
ropen.fd(768)
ropen.lt(90)
ropen.fd(432)
ropen.lt(90)
ropen.penup()
ropen.ht()
ropen.setundobuffer(1)
ropen.setposition(380,216)
ropen.pendown()
ropen.fd(84) # 84 +  768
ropen.rt(90)
ropen.fd(432)
ropen.rt(90)
ropen.fd(80)
ropen.penup()
ropen.setposition(460, 0)
ropen.pendown()
ropen.fd(75)
turtle.tracer(0)
global punkti
punkti = 0
rez = turtle.Turtle()
rez.speed(0)
rez.color("black")
rez.penup()
rez.setposition(300, 230)
rezstreng = "Punkti: %s" %punkti
rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
rez.hideturtle()
global lives
lives = 10
rez1 = turtle.Turtle()
rez1.speed(0)
rez1.color("black")
rez1.penup()
rez1.setposition(-350, 230)
rez1streng = "Lives: %s" %lives
rez1.write(rez1streng, False, align="left", font=("Arial", 20, "normal"))
rez1.hideturtle()
beg = 0
class sprite(turtle.Turtle):
    def __init__(self, forma, color, stx, sty):
        turtle.Turtle.__init__(self, shape = forma)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(stx, sty)
        self.speed = 1
    def move(self):
        self.fd(self.speed)


        if self.xcor() > 374:
            self.setx(374)
            self.rt(60)
        if self.xcor() < -374:
            self.setx(-374)
            self.rt(60)
        if self.ycor() > 206:
            self.sety(206)
            self.rt(60)
        if self.ycor() < -206:
            self.sety(-206)
            self.rt(60)
    def varsatr(t1, t2):
        dis = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
        if dis < beg:
                return True
        else:
                return False
    def ieksa(t1, t2):
        dis = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
        if dis < 20:
                return True
        else:
                return False

        
class Play(sprite):
    def __init__(self, forma, color, stx, sty):
        sprite.__init__(self, forma, color, stx, sty)
        self.speed = 3
        self.shapesize(stretch_wid=1, stretch_len= 1, outline = None)
        self.money = 0
    def turle(self):
        self.lt(45)
    def turla(self):
        self.rt(45)
    def priek(self):
        if self.speed < 8:
            self.speed += 1
    def atpak(self):
        if self.speed > -8:
            self.speed -= 1
    
        
    def move(self):
        self.fd(self.speed)
        if self.xcor() > 450:
            self.setx(450)
            self.speed = 0
            self.rt(180)
        if self.xcor() < -374:
            self.setx(-374)
            self.rt(60)
        if self.ycor() > 206:
            self.sety(206)
            self.rt(60)
        if self.ycor() < -206:
            self.sety(-206)
            self.rt(60)
class enem(sprite):
        def __init__(self, forma, color, stx, sty):
                sprite.__init__(self, forma, color, stx, sty)
                self.speed = 3
                self.setheading(random.randint(0, 360))

#def buy():
#    if play.xcor() > 384:
#        punkti -= 10
def buy():
    if play.xcor() > 384:
        if play.ycor() > 0:
            global punkti
            if punkti > 1000:
                punkti -= 1000
            global beg
            beg += 10
    
play = Play("firebal.gif", "red", 0, 0)
enemies = []
foo = ["circle", "square", "triangle"]
for e in range(15):
    enemies.append(enem((random.choice(foo)), "blue", random.randint(-350, 350), random.randint(-180, 180)))

turtle.onkey(play.turle, "a")
turtle.onkey(play.turla, "d")
turtle.onkey(play.priek, "w")
turtle.onkey(play.atpak, "s")
turtle.onkey(buy, "space")
turtle.listen()

while True:
    if play.heading() > -45 and play.heading() < 45:
        play.setsh("lej.gif")
    rezstreng = "Punkti: %s" %punkti
    rez.clear() 
    rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
    rez1streng = "Lives: %s" %lives
    rez1.clear() 
    rez1.write(rez1streng, False, align="left", font=("Arial", 20, "normal"))
    if play.xcor() < 384:
        punkti += 1

    turtle.update()
    time.sleep(0.015)
    play.move()
    for ene in enemies:
        ene.move()
        ene.speed = 2
        

                #satr?
        if play.varsatr(ene):
                        # SPELETAJA SKATIENS uZ KURU PUSI
            sps= play.heading()
            atr = play.speed
            ene.setheading(random.randint(sps - 45, sps + 45))
            ene.speed = atr * 2
        if play.ieksa(ene):
            lives -= 1
            x = random.randint(-350, 350)
            y = random.randint(-180, 180)
            ene.goto(x, y)
            punkti += random.randint(50, 100)


                #lode un pret
                #if lode1.ieksa(ene):
                 #       x = random.randint(-350, 350)
                  #      y = random.randint(-180, 180)
                   #     ene.goto(x, y)
                    #    punkti += random.randint(50, 100)
                     #   rezstreng = "Punkti: %s" %punkti
                      #  rez.clear() 
                       # rez.write(rezstreng, False, align="left", font=("Arial", 20, "normal"))


