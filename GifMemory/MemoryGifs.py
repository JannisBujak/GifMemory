
from json import JSONDecodeError
import sys, pygame
from turtle import Screen

import random
import json

from FieldInfo import FieldInfo, Field
from GIFImage import GIF_Image


framepercent = 0.05

def default_image():
    #return pygame.image.load("img/questionmark.jpg")
    default = GIF_Image("img/questionmark.jpg")
    return default

def createFields(fields_horiz, fields_vert, imagenames = []):
    local_fields = []
    for i in range(fields_horiz*fields_vert):
        if len(imagenames) <= (2*i):
            local_fields.append("fuesse_baumeln.gif")
        else:
            local_fields.append(imagenames[i*2])
    random.shuffle(local_fields)
    return local_fields
            
def drawPlayfield(playfield : Field, screen):
    
    coordwidth, coordheight = screen.get_size()
    cardwidth = coordwidth/playfield.width
    cardheight = coordheight/playfield.height
    
    for y in range(playfield.height):
        for x in range(playfield.width):
            field = playfield.getFieldAt(x, y)
            if field is not None:
                gif = field.getImage() if field.isOpen() else default_image()
                fieldimg = gif.getFrame(int(pygame.time.get_ticks() *15 / 1000))
                fieldimg = pygame.transform.scale(fieldimg, (cardwidth*(1-2*framepercent), cardheight*(1-2*framepercent)))
                screen.blit(fieldimg, ((x+framepercent)*cardwidth, (y+framepercent)*cardheight))
            

def reactToClick(playfield : Field, screen, x : int, y : int):
    winwidth, winheight = screen.get_size()
    cardwidth = winwidth/playfield.width
    cardheight = winheight/playfield.height
    opened_field = playfield.openAt(x/cardwidth, y/cardheight)

def main():
    size = width, height = 1500, 750
    
    black = 0, 0, 0

    #imagenames = [ "img/fuesse_baumeln.gif", "img/bird-snuggle.gif" ]
    
    f = open('init.json')
  
    # returns JSON object as a dictionary
    data = json.load(f)
    
    pics_vert, pics_horz = imagecount = data["imagecount"]
    imagenames = data["images"]

    pygame.init()

    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    playfield = Field(pics_horz, pics_vert)
    playfield.createFields(imagenames)

    drawPlayfield(playfield, screen)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                reactToClick(playfield, screen, x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playfield.restart()            

        screen.fill(black)
        drawPlayfield(playfield, screen)
        
        myfont = pygame.font.SysFont("monospace", 15)
        score = [0, 0]
        label1 = myfont.render(f"Player 1:  {score[0]}", 1, (255,255,255))
        screen.blit(label1, (100, 30))
        label2 = myfont.render(f"Player 2:  {score[1]}", 1, (255,255,255))
        screen.blit(label2, (1400, 30))

        pygame.display.flip()



if __name__ == "__main__":
    main()