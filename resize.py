from PIL import Image
import os, sys

path = "cards-old/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            im.thumbnail((300,300), Image.LANCZOS)
            im.save('cards/' + item, 'PNG')

resize()
