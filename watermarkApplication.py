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
        self.openImageButton = self.addButton(text="Open Image", row=0,
                                              column=1, command=self.openImage)
        self.imageList.append(self.addLabel(text="", row=1, column=2))
        self.photo = PhotoImage(file="blankImg.png")
        self.imageList[0]["image"] = self.photo

    def openImage(self):
        self.imageName = self.imageNameText.getText()
        print(self.imageName)

        self.photo = PhotoImage(file=self.imageName)
        self.imageList[0]["image"] = self.photo

def main():      
    Application().mainloop()

if __name__ == "__main__":
    main()
