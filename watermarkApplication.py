from PIL import Image
from breezypythongui import EasyFrame
from tkinter import PhotoImage
from tkinter import filedialog
import watermark
import os.path

class Application(EasyFrame):

    def __init__(self):

        EasyFrame.__init__(self, title="Watermarking", width=1920, height=1080)

        self.imageList = []
        self.imageName = ""
        self.wmName = ""
        self.splWord = "/"
        self.location = "1"

        self.blankImg = Image.new("RGB", (600,600))
        self.px_out = self.blankImg.load()

        for row in range(self.blankImg.size[0]):
            for col in range(self.blankImg.size[1]):
                self.px_out[row, col] = (0,0,0)

        self.blankImg.save("blankImg.png")

        self.imageNameButton = self.addButton(text="Browse for Image File", row=0, column=0,
                                            command=self.browseImgFiles)
        self.wmNameButton = self.addButton(text="Browse for Watermark File", row=1, column=0,
                                         command=self.browseWmFiles)

        self.imageNameLabel = self.addLabel(text="", row=0, column=1, sticky="NESW")
        self.wmNameLabel = self.addLabel(text="", row=1, column=1, sticky="NESW")
        
        self.openImageButton = self.addButton(text="Open Image", row=0,
                                              column=2, command=self.openImage)
        self.watermarkButton = self.addButton(text="Add Watermark", row=1,
                                              column=2,
                                              command=self.watermarkHelper)
        self.showWMButton = self.addButton(text="Show Watermark", row=2,
                                           column=2,
                                           command=self.showWatermarkHelper)
        self.locationTF = self.addTextField(text="Replace with 1,2,3, or 4 for watermark location",
                                            row=2, column=0, sticky="NESW")
        
        self.imageList.append(self.addLabel(text="", row=3, column=3))
        self.photo = PhotoImage(file="blankImg.png")
        self.imageList[0]["image"] = self.photo

    def changeLoc(self):
        if len(self.locationTF.getText()) == 1:
            self.location = self.locationTF.getText()
        else:
            self.location = "1"

    def openImage(self):
        self.resized_image = Image.open(self.imageName)
        self.resized_image.thumbnail((1000,1000), Image.Resampling.LANCZOS)
        self.resized_image.save("ImgResize.png")
        
        self.photo = PhotoImage(file="ImgResize.png")
        self.imageList[0]["image"] = self.photo

    def watermarkHelper(self):
        self.changeLoc()
        self.wtmk = Image.open(self.wmName)
        self.wtmk.convert("RGB")
        self.bits = 3
        self.img = Image.open(self.imageName)

        watermark.waterMark(self.img, self.wtmk, self.bits, self.location)

        self.resized_image = Image.open("watermarkedImg.png")
        self.resized_image.thumbnail((1000,1000), Image.Resampling.LANCZOS)
        self.resized_image.save("ImgResize.png")

        self.photo = PhotoImage(file="ImgResize.png")
        self.imageList[0]["image"] = self.photo

    def showWatermarkHelper(self):
        self.changeLoc()
        self.wtmk = Image.open(self.wmName)
        self.wtmk.convert("RGB")
        self.bits = 3
        self.img = Image.open(self.imageName)

        encode = watermark.waterMark(self.img, self.wtmk, self.bits, self.location)
        watermark.showWatermark(encode, self.wtmk.size, self.bits, self.location)

        self.resized_image = Image.open("watermarkedImg.png")
        self.resized_image.thumbnail((1000,1000), Image.Resampling.LANCZOS)
        self.resized_image.save("ImgResize.png")

        self.photo = PhotoImage(file="ImgResize.png")
        self.imageList[0]["image"] = self.photo

    def browseImgFiles(self):
        self.imageName = filedialog.askopenfilename(initialdir = "/", title="Selecct a File",
                                                   filetypes = (("Image files",
                                                                 "*.png *.jpeg"),
                                                                ("all files", "*.")))

        self.res = self.imageName.split(self.splWord, 15)
        self.imageNameLabel.configure(text="File: "+self.res[-1])
        
    def browseWmFiles(self):
        self.wmName = filedialog.askopenfilename(initialdir = "/", title="Selecct a File",
                                                   filetypes = (("Image files",
                                                                 "*.png *.jpeg"),
                                                                ("all files", "*.")))
        
        self.res = self.wmName.split(self.splWord, 15)
        self.imageNameLabel.configure(text="Image File: "+self.res[-1])
        self.wmNameLabel.configure(text="Watermark File: "+self.res[-1])

def main():      
    Application().mainloop()

if __name__ == "__main__":
    main()
