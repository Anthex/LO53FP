from structure import NLateration, Location
from math import floor, sqrt
from PIL import Image, ImageDraw

dataset = [(Location(.5,.5,.5), 3.0), (Location(4.0,.0,.0), 2.0), (Location(4.0,5.0,5.0), 4.2), (Location(3.0,3.0,3.0), 2.5)]
NLat_result = NLateration(dataset)
W,H = NLat_result[3], NLat_result[4]
frames = []

def createFrame(x,y,nbr):
    img = Image.new("L",(x,y))
    img.putdata(NLat_result[5][nbr])
    return img

def exportGif():
    for i in range(len(NLat_result[5])):
        newFrame = createFrame(W,H,i)
        newFrame = newFrame.resize((W*10,H*10), Image.ANTIALIAS)
        draw = ImageDraw.Draw(newFrame)
        draw.text(text="z="+str(i), xy=(0,0))
        frames.append(newFrame)

    frames[0].save("out.gif", format="GIF", append_images=frames[1:], save_all=True, duration=100, loop=0)
    print("gif exported")

