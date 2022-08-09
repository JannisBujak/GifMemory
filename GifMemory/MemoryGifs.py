
from concurrent.futures import thread
from datetime import datetime
from json import JSONDecodeError
import os, sys, pygame
from time import time
import threading
# from turtle import Screen

import random
import json

from FieldInfo import FieldInfo, Field
from GIFImage import GIF_Image

from PIL import Image
from PIL import GifImagePlugin

black = 0, 0, 0    

framepercentX = 0.05
framepercentY = 0.1

def filedir():
    return os.path.dirname(os.path.abspath(__file__))

def default_image():
    #return pygame.image.load("img/questionmark.jpg")
    default = GIF_Image(f"{filedir()}/img/questionmark.jpg")
    return default

def createFields(fields_horiz, fields_vert, imagenames = []):
    local_fields = []
    for i in range(fields_horiz*fields_vert):
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
                fieldimg = pygame.transform.scale(fieldimg, (cardwidth*(1-2*framepercentX), cardheight*(1-2*framepercentY)))
                screen.blit(fieldimg, ((x+framepercentX)*cardwidth, (y+framepercentY)*cardheight))
            

def reactToClick(playfield : Field, screen, x : int, y : int):
    winwidth, winheight = screen.get_size()
    cardwidth = winwidth/playfield.width
    cardheight = winheight/playfield.height
    opened_field = playfield.openAt(int(x/cardwidth), int(y/cardheight))
    
def precreateSubgifs(imagenames):
    gifs = []
    threads = []
    def addToGifs(filepath):
        gifs.append(GIF_Image(filepath))
    t_start = datetime.now()

    for imagename in imagenames:
        t = threading.Thread(target=addToGifs, args=(f"{filedir()}/{imagename}",))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
     
    t_end = datetime.now()
    t_diff = t_end-t_start
    print(f"Loading took {t_diff.seconds}{int(t_diff.microseconds/1000)} ms")

    return gifs


def renderLabel(i: int, screen, playfield):
    width, height = screen.get_size()
    font = pygame.font.SysFont("monospace", (int)((height/20)), bold=(playfield.active_player==i))
    
    label = font.render(f"Player {i}:  {playfield.player_scores[i]}", 1, (255,255,255))
    if i > 0:
        screen.blit(label, (width*(19/20)-label.get_width(), height/20))
    else:
        screen.blit(label, (width/20, height/20))
    

def adaptElementSizes(screen, playfield):
    screen.fill(black)
    drawPlayfield(playfield, screen)
    
    
    renderLabel(0, screen, playfield)
    renderLabel(1, screen, playfield)
    """
    width, height = screen.get_size()
    normalFont = pygame.font.SysFont("monospace", (int)(height/20))
    boldFont = pygame.font.Font(normalFont, bold=True)
    label1 = myfont.render(f"Player 1:  {playfield.player_scores[0]}", 1, (255,255,255))
    lw = label1.get_width()
    screen.blit(label1, (width/20, height/20))
    label2 = myfont.render(f"Player 2:  {playfield.player_scores[1]}", 1, (255,255,255))
    screen.blit(label2, ((int)(width*(19/20) - label2.get_width()), (int)(height/20)))
    """

def main():
    #imagenames = [ "img/fuesse_baumeln.gif", "img/bird-snuggle.gif" ]
    initial_size = 1500, 750
    f = open(f"{filedir()}/init.json")
  
    # returns JSON object as a dictionary
    data = json.load(f)
    
    pics_vert, pics_horz = imagecount = data["imagecount"]

    imagemap = precreateSubgifs(data["images"])

    pygame.init()

    screen = pygame.display.set_mode(initial_size, pygame.RESIZABLE)
    
    playfield = Field(pics_horz, pics_vert)
    playfield.createFields(imagemap)

    drawPlayfield(playfield, screen)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                reactToClick(playfield, screen, x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playfield.restart()            

        adaptElementSizes(screen, playfield)

        pygame.display.flip()



if __name__ == "__main__":
    main()