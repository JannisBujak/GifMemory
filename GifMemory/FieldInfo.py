
from dataclasses import field
import sys, pygame
from numpy import empty
import random
from GIFImage import GIF_Image

class FieldInfo:
    def __init__(self, id, imgpath) -> None:
        self.imgpath = imgpath
        self.isopen = False
        self.id = id
        img = GIF_Image(self.imgpath)

        #img = pygame.image.load(self.imgpath)
        self.img = img

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def reset(self):
        self.isopen = False

    def toggleOpen(self):
        self.isopen = not self.isopen
        #self.isopen = True

    def isOpen(self):
        return self.isopen

    def getImage(self) -> GIF_Image:
        return self.img


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = []
        self.openfields = []

    def createFields(self, imagenames = []):
        self.fields = []
        for i in range(self.width * self.height):
            id = int(i/2)
            if len(imagenames) <= id:
                self.fields.append(FieldInfo(id, "img/fuesse_baumeln.gif"))
            else:
                self.fields.append(FieldInfo(id, imagenames[id]))
        random.shuffle(self.fields)

    def restart(self):
        self.openfields = []
        for i in range (len(self.fields)):
            self.fields[i].reset()
        random.shuffle(self.fields)

    def getFieldAt(self, x : int, y : int) -> FieldInfo:
        adr = x + int(y*self.width)
        if x >= self.width or y >= self.height or adr >= len(self.fields):
            return None
        
        return self.fields[adr]

    def openAt(self, x : int, y : int):
        field = self.getFieldAt(int(x), int(y))
        if field is None or field.isOpen():
            return

        # nicht "doppelt" geklickt
        field.toggleOpen()

        if len(self.openfields) > 1:
            # close temporarily opened images
            for f in self.openfields:
                f.reset()
            self.openfields = []

        elif len(self.openfields) == 1:
            if field == self.openfields[0]:
                # success, temporarily opened Images stay opened
                self.openfields = []
            else:
                self.openfields.append(field)
        else:
            # no temporarily opened Image yet
            self.openfields.append(field)


        


    