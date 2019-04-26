import os
from visuals import createFrame, exportGif
from PIL import Image

def test_createFrame():
    result = createFrame(100,100,1)
    assert type(result) is Image.Image

def test_exportGif():
    exportGif()
    assert os.path.exists("./out.gif")
