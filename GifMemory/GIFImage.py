
from operator import mod
from PIL import Image
from PIL import GifImagePlugin

import os

import sys, pygame

class GIF_Image:
    def __init__(self, filepath) -> None:
        imageObj = Image.open(filepath)
        self.num_frames = 1
        self.images = []
        tryget = getattr(imageObj, "is_animated", None)

        if tryget is None or not tryget:
            self.images.append(pygame.image.load(filepath))
        else:
            self.num_frames = imageObj.n_frames
            for i in range(self.num_frames):
                imageObj.seek(i)
                new_path = self.buildNewFilename(filepath, i+1)
                imageObj.save(new_path)
                self.images.append(pygame.image.load(new_path))

        imageObj.close()

            
    def buildNewFilename(self, oldFn: str, i: int):
        pathname, ext = oldFn.rsplit(".", 1) 
        path_name = pathname.rsplit("/", 1)
        
        path, name = [f"{path_name[0]}/out/", path_name[1]] if (len(path_name) > 1) else ["./out/", path_name[0]]
        os.makedirs(path, exist_ok=True)
        
        pathname = f"{path}.{name}"
        
        return f"{pathname}{i}.{ext}"


    def getFrame(self, i: int):
        return self.images[mod(i, self.num_frames)]
        

    
