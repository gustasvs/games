import os
import turtle
import math
import random
#skreen
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("spele")
#wn.bgpic("gwwpp.png")

        

#robeza
ropen = turtle.Turtle()
ropen.speed(0)
ropen.color("black")
ropen.penup()
ropen.setposition(-300,-300)
ropen.pendown()
ropen.pensize(4)
for e in range(4):
        ropen.fd(600)
        ropen.lt(90)
ropen.penup()
ropen.setposition(-300, -120)
ropen.pendown()
ropen.fd(600)
ropen.hideturtle()
ropen.penup()

punkti = 0
rez = turtle.Turtle()
rez.speed(0)
rez.color("black")
rez.penup()
rez.setposition(300, 290)
rezstreng = "Punkti: %s" %punkti
rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))

#speletajs
play = turtle.Turtle()
play.color("blue")
play.shape("triangle")
play.speed(0)
play.penup()
play.setposition(0, -250)
play.setheading(90)

#pretin
ene = turtle.Turtle()
ene.color("red")
ene.shape("circle")
ene.penup()
ene.speed(0)
ene.setposition(0, 250)
enesped = 4
ene.shapesize(3, 3)

playsped = 20
#lode
lode = turtle.Turtle()
lode.color("black")
lode.penup()
lode.speed(0)
lode.shape("triangle")
lode.setheading(90)
lode.shapesize(0.5, 0.5)
lode.hideturtle()
lodesped = 25


lodstav = "gatav" 
#move -[palyer

def moveleft():
        x = play.xcor()
        x -= playsped
        if x < -280:
                x=-280
        play.setx(x)
def moveright():
        x = play.xcor()
        x += playsped
        if x > 280:
                x = 280
        play.setx(x)
def movedown():
        y = play.ycor()
        y += playsped
        if y > -140:
                y = -140
        play.sety(y)
def moveup():
        y = play.ycor()
        y -= playsped
        if y < -280:
                y = -280
        play.sety(y)
def sauj():
        global lodstav
        if lodstav == "gatav":
                lodstav = "saut"
                x = play.xcor()
                y = play.ycor()
                lode.setpos(x, y + 10)
                lode.showturtle()


def varsatr(t1, t2):
        dis = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
        if dis < 30:
                return True
        else:
                return False



#bindings
turtle.listen()
turtle.onkey(moveleft, "a")
turtle.onkey(moveright, "d")
turtle.onkey(movedown, "w")
turtle.onkey(moveup, "s")
turtle.onkey(sauj, "space")


#meinlups
while True:

                
        x = ene.xcor()
        x += enesped
        ene.setx(x)
        if ene.xcor() > 280:
                enesped *= -1
                y = ene.ycor()
                y -= 20
                ene.sety(y)
        if ene.xcor() < -280:
                enesped*= -1
                y = ene.ycor()
                y -= 20
                ene.sety(y)
        y = lode.ycor()
        y += lodesped
        lode.sety(y)
        if lode.ycor() > 285:
                lode.hideturtle()
                lodstav = "gatav"
        if varsatr(lode, ene):
               lode.hideturtle()
               lodstav = "ready"
               lode.setposition(400, 0)
               ene.setposition(0, 250)
               punkti += random.randint(50, 100)
               rezstreng = "Punkti: %s" %punkti
               rez.clear() 
               rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
               
        if varsatr(play, ene):
                punkti -= random.randint(900, 1000)
                rezstreng = "Punkti: %s" %punkti
                rez.clear() 
                rez.write(rezstreng, False, align="left", font=("Gulim", 20, "normal"))
        if punkti > 200:
                punkte = "UZVARA"
                rezstreng = "%s" %punkte
                rez.clear() 
                rez.write(rezstreng, False, align="left", font=("Gulim", 100, "normal"))
                rez.setposition(-400, 0)
                ropen.clear()
                ene.hideturtle()
                play.shapesize(10, 10)
                play.color("red")
        print(punkti)
                
               

delay = input("enteeer")

