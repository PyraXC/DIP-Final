from PIL import Image
from breezypythongui import EasyFrame
from tkinter import PhotoImage
import watermark
import os.path

class Application(EasyFrame):

    def __init__(self):

        EasyFrame.__init__(self, title="Watermarking", width=1920, height=1080)

        self.imageList = []
        self.imageName = ""

        self.blankImg = Image.new("RGB", (600,600))
        self.px_out = self.blankImg.load()

        for row in range(self.blankImg.size[0]):
            for col in range(self.blankImg.size[1]):
                self.px_out[row, col] = (0,0,0)

        self.blankImg.save("blankImg.png")

        self.imageNameText = self.addTextField("", row=0, column=0,sticky="NESW")
        self.wmNameText = self.addTextField("", row=1, column=0, sticky="NESW")
        self.openImageButton = self.addButton(text="Open Image", row=0,
                                              column=1, command=self.openImage)
        self.watermarkButton = self.addButton(text="Add Watermark", row=1,
                                              column=1,
                                              command=self.watermarkHelper)
        self.showWMButton = self.addButton(text="Show Watermark", row=2,
                                           column=1,
                                           command=self.showWatermarkHelper)
        self.imageList.append(self.addLabel(text="", row=3, column=2))
        self.photo = PhotoImage(file="blankImg.png")
        self.imageList[0]["image"] = self.photo

    def openImage(self):
        self.imageName = self.imageNameText.getText()
        print(self.imageName)

        self.photo = PhotoImage(file=self.imageName)
        self.imageList[0]["image"] = self.photo

    def watermarkHelper(self):
        self.wtmk = Image.open(self.wmNameText.getText())
        self.wtmk.convert("RGB")
        self.bits = 3
        self.img = Image.open(self.imageName)

        watermark.waterMark(self.img, self.wtmk, self.bits)

        self.photo = PhotoImage(file="watermarkedImg.png")
        self.imageList[0]["image"] = self.photo

    def showWatermarkHelper(self):
        self.wtmk = Image.open(self.wmNameText.getText())
        self.wtmk.convert("RGB")
        self.bits = 3
        self.img = Image.open(self.imageName)

        encode = watermark.waterMark(self.img, self.wtmk, self.bits)
        watermark.showWatermark(encode, self.wtmk.size, self.bits)

        self.photo = PhotoImage(file="watermarkedImg.png")
        self.imageList[0]["image"] = self.photo

def main():      
    Application().mainloop()

if __name__ == "__main__":
    main()
