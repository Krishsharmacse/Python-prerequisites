import pygame as p
x = p.init()
gamewindow = p.display.set_mode((1200,500))
p.display.set_caption("My First Game")
exit_game = False
game_over = False
#game loop
while not exit_game:
    for event in p.event.get():
        if event.type==p.QUIT:
            exit_game = True
        if event.type==p.KEYDOWN:
            if event.key == p.K_RIGHT:
                print("you press right")
    

p.quit()
quit()

