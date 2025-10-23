import turtle
from turtle import *
screen = turtle.Screen()

# Defining a turtle Instance
t = turtle.Turtle()
speed(0)

# # initially penup()
t.penup()
t.goto(-400, 250)
t.pendown()

# # Orange Rectangle 
# #white rectangle
t.color("orange")
t.begin_fill()
t.forward(750)
t.right(90)
t.forward(150)
t.right(90)
t.forward(750)
t.end_fill()
t.left(90)
t.forward(200)