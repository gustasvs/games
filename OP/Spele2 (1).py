import os
import turtle
import random
import math
import winsound
import time
wn = turtle.Screen()
wn.bgcolor("lightblue")
wn.title("spele")
wn.bgpic("bce.gif")
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
ropen.penup()
ropen.setposition(460, 108)
ropen.pendown()
ropen.fd(75)
ropen.penup()
ropen.setposition(460, -108)
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
rez.write(rezstreng, False, align="left", font=("Gulim", 20, "bold"))
rez.hideturtle()

global lives
lives = 10
rez1 = turtle.Turtle()
rez1.speed(0)
rez1.color("black")
rez1.penup()
rez1.setposition(-350, 230)
rez1streng = "Lives: %s" %lives
rez1.write(rez1streng, False, align="left", font=("Arial", 20, "bold"))
rez1.hideturtle()

global kopi1
kopi01 = turtle.Turtle()
kopi01.speed(0)
kopi01.color("black")
kopi01.penup()
kopi01.setposition(-200, 230)
kopi01streng = "Buy Force Field for 1000 Points"
#kopi01.write(kopi01streng, False, align="left", font=("Arial", 20, "normal"))
kopi01.hideturtle()


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
    def liieks(self, cits):
        if (self.xcor() > (cits.xcor() - 80)) and (self.xcor() < (cits.xcor() + 80)): 
            if self.ycor() <= cits.ycor() + 10 and self.ycor() >= cits.ycor() - 10:
                return True
            else:
                return False
    def ieksq(t1, t2):
        dis = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
        if dis < 100:
                return True
        else:
                return False

        
class Play(sprite):
    def __init__(self, forma, color, stx, sty):
        sprite.__init__(self, forma, color, stx, sty)
        self.speed = 3
        self.shapesize(stretch_wid=1, stretch_len= 1, outline = None)
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
class linija(sprite):
    def __init__(self, forma, color, stx, sty):
        sprite.__init__(self, forma, color, stx, sty)
    def move(self):
        self.setheading(-90)
        self.fd(self.speed)
        self.shapesize(stretch_wid=6, stretch_len= 1, outline = None)
        self.speed = 3
        if self.ycor() > 500:
            self.sety(500)
        if self.ycor() < -500:
            self.sety(500)
def buy():
    if play.xcor() > 384:
        if play.ycor() > 108:
            global punkti
            if punkti > 1000:
                punkti -= 1 ##############################
            global beg
            beg += 10
    if play.xcor() > 384:
        if play.ycor() > 0 and play.ycor() < 108:
            if punkti > 200:
                punkti -= 200
                global lives
                lives += 1
class bumbe(sprite):
    def __init__(self, forma, color, stx, sty):
        sprite.__init__(self, forma, color, stx, sty)
        #self.hideturtle()
    def move(self):

        x = play.xcor()
        y = play.ycor()
        self.setposition(x, y)
        

bumba = bumbe("triangle", "black", 0, 0)   
play = Play("triangle", "red", 0, 0)
enemies = []
foo = ["circle", "square", "triangle"]
for e in range(15):
    enemies.append(enem((random.choice(foo)), "blue", random.randint(-350, 350), random.randint(-180, 180)))
garie = []
for e in range(5): 
    garie.append(linija("square", "blue", random.randint(-400, 400), random.randint(400, 800)))

turtle.onkey(play.turle, "a")
turtle.onkey(play.turla, "d")
turtle.onkey(play.priek, "w")
turtle.onkey(play.atpak, "s")
turtle.onkey(buy, "space")
turtle.onkey(bumba.move, "e")
turtle.listen()

while True:
    rezstreng = "Punkti: %s" %punkti
    rez.clear() 
    rez.write(rezstreng, False, align="left", font=("Gulim", 20, "bold"))
    rez1streng = "Lives: %s" %lives
    rez1.clear() 
    rez1.write(rez1streng, False, align="left", font=("Arial", 20, "bold"))
    if play.xcor() < 384:
        punkti += 1
        kopi01streng =""
        kopi01.clear() 
        kopi01.write(kopi01streng, False, align="left", font=("Arial", 20, "bold"))
    if play.xcor() > 384:
        if play.ycor() > 108:
                kopi01streng ="Buy Force Field for 1000 Points"
                kopi01.clear() 
                kopi01.write(kopi01streng, False, align="left", font=("Arial", 20, "bold"))
    if play.xcor() > 384:
        if play.ycor() > 0 and play.ycor() < 108:
                kopi01streng ="Buy Lives for 200 Points"
                kopi01.clear() 
                kopi01.write(kopi01streng, False, align="left", font=("Arial", 20, "bold"))
            
    turtle.update()
    time.sleep(0.015)
    play.move()
    
    for ene in enemies:
        ene.move()
        ene.speed = 2
        
        if bumba.ieksq(ene): ########### VAIG BUMBA SPRAG
            sps= play.heading()
            atr = play.speed
            ene.setheading(random.randint(sps - 35, sps + 35))
            ene.speed = atr * 2
        if play.varsatr(ene):
            sps= play.heading()
            atr = play.speed
            ene.setheading(random.randint(sps - 45, sps + 45))
            ene.speed = atr * 2
        if play.ieksa(ene):
            lives -= 0##############################################
            x = random.randint(-350, 350)
            y = random.randint(-180, 180)
            ene.goto(x, y)
            #punkti -= random.randint(50, 100)
    for gar in garie:
        gar.move()
        gar.speed = random.randint(1, 3)
        if play.liieks(gar):
            gar.setposition(random.randint(-400, 330), 500)
