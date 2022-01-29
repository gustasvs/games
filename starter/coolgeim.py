import os
import turtle
import random
import math
import winsound
import time
beg = 50
#ekrans
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("spele")
#wn.bgpic("gwwpp.png")
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
turtle.tracer(0)

punkti = 0
rez = turtle.Turtle()
rez.speed(0)
rez.color("black")
rez.penup()
rez.setposition(300, 290)
rezstreng = "Punkti: %s" %punkti
rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
rez.hideturtle()

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
        # ka satriecas
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
                self.speed += 1
        def atpak(self):
                self.speed -= 1
class enem(sprite):
        def __init__(self, forma, color, stx, sty):
                sprite.__init__(self, forma, color, stx, sty)
                self.speed = 3
                self.setheading(random.randint(0, 360))
                

class game():
        def __init__(self):
                self.level = 1
                self.score = 0
                self.state = "playing"
class lode1(sprite):
        def __init__(self, forma, color, stx, sty):
                sprite.__init__(self, forma, color, stx, sty)
                self.speed = 20
                self.shapesize(stretch_wid=0.3, stretch_len= 0.3, outline = None)
                self.status = "ready"
                self.goto(1000, 1000)
        def sauj(self):
                if self.status == "ready":
                        self.goto(play.xcor(), play.ycor())
                        self.setheading(play.heading())
                        self.status = "saujas"
        def move(self):
                if self.status == "ready":
                        self.goto(1000, 1000)        
                if self.status == "saujas":
                        self.fd(self.speed)
                        #cik ilgi lode lido
                        if self.xcor() < -500 or self.xcor() > 500 or self.ycor() < -500 or self.ycor() > 500:
                                self.status = "ready"
                                self.goto(1000, 1000)

                                #OTRAA LODE
class lode2(sprite):
        def __init__(self, forma, color, stx, sty):
                sprite.__init__(self, forma, color, stx, sty)
                self.speed = 20
                self.shapesize(stretch_wid=0.3, stretch_len= 0.3, outline = None)
                self.status = "ready"
                self.goto(1000, 1000)
        def sauj(self):
                if self.status == "ready":
                        #skana
                        winsound.PlaySound("YOU SUCK.wav", winsound.SND_ASYNC)
                        
                        self.goto(play.xcor(), play.ycor())
                        self.setheading(play.heading() - 180)
                        self.status = "saujas"
        def move(self):
                if self.status == "ready":
                        self.goto(1000, 1000)        
                if self.status == "saujas":
                        self.fd(self.speed)
                        #cik ilgi lode lido
                        if self.xcor() < -500 or self.xcor() > 500 or self.ycor() < -500 or self.ycor() > 500:
                                self.status = "ready"
                                self.goto(1000, 1000)
class particle(sprite):
        def __init__(self, forma, color, stx, sty):
                sprite.__init__(self, forma, color, stx, sty)
                self.shapesize(stretch_wid=0.1, stretch_len= 0.1, outline = None)
                self.goto(1000,1000)
                self.frame = 0
        def explod(self, stx, sty):
                self.goto(stx, sty)
                self.setheading(random.randint(0, 360))
        def move(self):
                if self.frame > 0:
                        self.fd(9)
                if self.frame > 20:
                        self.frame = 0
                        self.goto(1000, 1000)
                
                        
                
Game = game()
 
#izvedot spreitus
play = Play("circle", "red", 0, 0)
#ene = enem("circle", "blue", 0, 100)
lode1 = lode1("circle", "orange", 0, 0)
lode2 = lode2("circle", "red", 0, 0)
particles = []
for e in range(20):
        particles.append(particle("square", "red", 0, 0))
enemies = []
foo = ["circle", "square", "triangle"]
for e in range(15):
        enemies.append(enem((random.choice(foo)), "blue", 0, 100))
        

#bindengs

turtle.onkey(play.turle, "a")
turtle.onkey(play.turla, "d")
turtle.onkey(play.priek, "w")
turtle.onkey(play.atpak, "s")
turtle.onkey(lode1.sauj, "q")
turtle.onkey(lode2.sauj, "space")
turtle.listen()



#meilup
while True:
        punkti += 1
        rezstreng = "Punkti: %s" %punkti
        rez.clear() 
        rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
        
        turtle.update()
        time.sleep(0.015)
        play.move()
        lode1.move()
        lode2.move()
        #ene.move()
        #ene.speed = 4
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
                        x = random.randint(-350, 350)
                        y = random.randint(-180, 180)
                        ene.goto(x, y)
                        punkti += random.randint(50, 100)
                        rezstreng = "Punkti: %s" %punkti
                        rez.clear() 
                        rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
                        for particle in particles:
                                particle.goto(lode1.xcor(), lode1.ycor())
                                particle.setheading(random.randint(0, 360))
                        for particle in particles:
                                particle.move()

                #lode un pret
                if lode1.ieksa(ene):
                        x = random.randint(-350, 350)
                        y = random.randint(-180, 180)
                        ene.goto(x, y)
                        punkti += random.randint(50, 100)
                        rezstreng = "Punkti: %s" %punkti
                        rez.clear() 
                        rez.write(rezstreng, False, align="left", font=("Arial", 20, "normal"))
                        winsound.PlaySound("KOBE.wav", winsound.SND_ASYNC)
                        #part
                        for particle in particles:
                                particle.goto(lode1.xcor(), lode1.ycor())
                                particle.setheading(random.randint(0, 360))
                                particle.explod(lode1.xcor(), lode1.ycor())

                                

                if lode2.ieksa(ene):
                        x = random.randint(-350, 350)
                        y = random.randint(-180, 180)
                        ene.goto(x, y)
                        punkti += random.randint(50, 100)
                        rezstreng = "Punkti: %s" %punkti
                        rez.clear() 
                        rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
                        winsound.PlaySound("KOBE.wav", winsound.SND_ASYNC)
                        #part
                        for particle in particles:
                                particle.goto(lode2.xcor(), lode2.ycor())
                                particle.explod(lode1.xcor(), lode1.ycor())
                                particle.move()

                
                        
        









rel = input("lol")
