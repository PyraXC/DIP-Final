import numpy as np
from PIL import Image
MAX_BIT_VALUE = 8
MAX_COLOR_VALUE = 256

def createImage(data, img, size, wtmks):
    #img = Image.new("RGB", size)
    #image = img.load()
    image = img.load()
    i = 0
    #print(len(data))
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            if x < wtmks[0] and y < wtmks[1]:
                image[x, y] = data[i]
                i+=1

    img.save("watermarkedImg.png")
    return img

def mostSigBits(num, bits):
    return num >> MAX_BIT_VALUE - bits

def leastSigBits(num, bits):
    num = num << MAX_BIT_VALUE - bits
    num = num % MAX_COLOR_VALUE
    return num >> MAX_BIT_VALUE - bits

def delLeastSigBits(num, bits):
    num = num >> bits
    return num << bits

def returnBits(num, bits):
    return num << MAX_BIT_VALUE - bits

def check_gray(img):
    temp = img[0,0]
    if isinstance(temp, int):
        return True
    else:
        return False
def toRGB(img):
    image = img.load()
    RGB = Image.new('RGB', (img.size[0], img.size[1]))
    rgb = RGB.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            temp = image[x,y]
            rgb[x,y] = (temp, temp, temp)
    #print(rgb[0,0])
    return RGB

def waterMark(img, wtmk, bits):
    imgx, imgy = img.size
    wtmkx, wtmky = wtmk.size
    px_in = img.load()
    px_hide = wtmk.load()
    if wtmkx > imgx or wtmky > imgy:
        print("watermark too big")
        return
    if(check_gray(px_in)):
        img = toRGB(img)
        px_in = img.load()

    if(check_gray(px_hide)):
        wtmk = toRGB(wtmk)
        px_hide = wtmk.load()

    temp = []
    for row in range(wtmkx):
        for col in range(wtmky):
            #print(px_hide[row, col])
            r, g, b = px_hide[row, col]
            r = mostSigBits(r, bits)
            g = mostSigBits(g, bits)
            b = mostSigBits(b, bits)
            
            lr, lg, lb = px_in[row, col]
            lr = delLeastSigBits(lr, bits)
            lg = delLeastSigBits(lg, bits)
            lb = delLeastSigBits(lb, bits)

            temp.append((lr + r, lg + g, lb + b))

    return createImage(temp, img, (imgx, imgy),  (wtmkx, wtmky))

def showWatermark(img, wtmks, bits):
    width = img.size[0]
    height = img.size[1]
    image = img.load()

    temp = []

    for row in range(wtmks[0]):
        for col in range(wtmks[1]):

            r, g, b = image[row,col]
            
            r = leastSigBits(r, bits)
            g = leastSigBits(g, bits)
            b = leastSigBits(b, bits)

            r = returnBits(r, bits)
            g = returnBits(g, bits)
            b = returnBits(b, bits)

            temp.append((r, g, b))

    return createImage(temp, img, img.size, wtmks)
            
def main():
    wtmk = Image.open("lena_gray_512.png")
    #wtmk.convert("RGB")
    img = Image.open("thumbnail.png")
    #img.convert("RGB")
    bits = 3
    encode = waterMark(img, wtmk, bits)
    encode.show()
    decode = showWatermark(encode, wtmk.size, bits)
    decode.show()

if "__main__":
    main()
