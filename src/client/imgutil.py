from PIL import Image

def tobitmap(data, width, height):
    ''' Converts to the X11 bitmap format via PIL. '''
    
    img = Image.frombytes(mode='1', size=(width,height), data=bytes(data))
    
    return img.tobitmap()
