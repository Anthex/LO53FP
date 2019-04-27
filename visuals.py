from structure import NLateration, Location
from math import floor, sqrt
from PIL import Image, ImageDraw

global_step=.1
dataset = [(Location(.5,.5,.5), 3.0), (Location(4.0,.0,.0), 2.0), (Location(4.0,5.0,5.0), 4.2)]
NLat_result = NLateration(dataset, step=global_step)
W,H = NLat_result[3], NLat_result[4]
frames = []
dummy = [0 for _ in range(len(NLat_result[5][0]))]

def createFrame(x,y,nbr):
    img = Image.new("HSV",(y,x))
    img.putdata(NLat_result[5][nbr])
    return img


def exportGif():
    for i in range(len(NLat_result[5])):
        newFrame = createFrame(W,H,i)
        newFrame = newFrame.resize((W*10,H*10), Image.BICUBIC)
        draw = ImageDraw.Draw(newFrame)
        draw.text(text="z="+str(round(i*global_step,2)), xy=(0,0))
        frames.append(newFrame)
    
    for i in range(len(NLat_result[5])):
        newFrame = createFrame(W,H,len(NLat_result[5])-i-1)
        newFrame = newFrame.resize((W*10,H*10), Image.ANTIALIAS)
        draw = ImageDraw.Draw(newFrame)
        draw.text(text="z="+str(round(((len(NLat_result[5])-i-1)*global_step),2)), xy=(0,0))
        frames.append(newFrame)
    
    frames[0].save("out.gif", format="GIF", append_images=frames[1:], save_all=True, duration=20, loop=0)
    print("gif exported")

exportGif()