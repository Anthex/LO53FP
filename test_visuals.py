import os
from visuals import createFrame, exportGif
from PIL import Image

def test_createFrame():
    result = createFrame(100,100,[(0,0,0)],0)
    assert isinstance(result, Image.Image)

def test_exportGif():
    exportGif()
    assert os.path.exists(os.getcwd()+"/out.webp")
