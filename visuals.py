print("Importing Libs")
from structure import NLateration, Location
from math import floor
from PIL import Image, ImageDraw
import sys
import time

global_step=.05
upscale_factor=1
upscale_method = Image.NEAREST
dataset = [(Location(.5,.5,0), 3.0), (Location(5.0,7.0,.0), 4.0), (Location(3.0,.0,5.0), 4)]
colorRange=1.0 # [0.0, 1.0]
#NLat_result = NLateration(dataset, step=global_step)

frames = []
max = NLateration(dataset, step=global_step)

def createFrame(x,y,arr,nbr):
    img = Image.new("HSV",(y,x))
    img.putdata(arr[nbr])
    return img


def exportGif(includeReverse=False):
    print(str(round(1000*(time.time()-start),2))+"ms"," - Calculating Array")
    NLat_result = NLateration(dataset, step=global_step,  md=max[1], dmax=max[6]*colorRange)
    W,H = NLat_result[3], NLat_result[4]
    print(str(round(1000*(time.time()-start),2))+"ms"," - Generating gif/video")

    for i in range(len(NLat_result[5])):
        print(".", end="")
        sys.stdout.flush()
        newFrame = createFrame(W,H,NLat_result[5],i)
        newFrame = newFrame.resize((W*upscale_factor,H*upscale_factor), upscale_method)
        draw = ImageDraw.Draw(newFrame)
        draw.text(text="z="+str(round(i*global_step,2)), xy=(0,0))
        frames.append(newFrame)
    
    if includeReverse:
        for i in range(len(NLat_result[5])):
            print(".", end="")
            sys.stdout.flush()
            newFrame = createFrame(W,H,NLat_result[5],len(NLat_result[5])-i-1)
            newFrame = newFrame.resize((W*upscale_factor,H*upscale_factor), upscale_method)
            draw = ImageDraw.Draw(newFrame)
            draw.text(text="z="+str(round(((len(NLat_result[5])-i-1)*global_step),2)), xy=(0,0))
            frames.append(newFrame)
        
    print(str(round(1000*(time.time()-start),2))+"ms","saving gif/video",)
    #frames[0].save("out.gif", format="GIF", append_images=frames[1:], save_all=True, duration=20, loop=0)
    frames[0].save("../../chat/out.webp", format="WebP", append_images=frames[1:], save_all=True, duration=40, lossless=True)
    print(str(round(1000*(time.time()-start),2))+"ms","gif exported")

start = time.time()
exportGif(True)