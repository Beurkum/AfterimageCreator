from PIL import ImageTk, Image
import PIL.ImageOps
import tkinter as tk
import glob
import os

# -------FUNCTIONS-------

def checkForNecessaryElements():
    os.chdir("./")
    file = glob.glob("*.jpeg")
    if "grayscale.jpeg" and "inverted.jpeg" in file:
        image = Image.open("grayscale.jpeg")
        WIDTH, HEIGHT = image.size
        return WIDTH, HEIGHT
    else:
        file = glob.glob("*.jpg")
        if "grayscale.jpg" and "inverted.jpg" in file:
            image = Image.open("grayscale.jpg")
            WIDTH, HEIGHT = image.size
            return WIDTH, HEIGHT
        else:
            file = glob.glob("*.png")
            if "grayscale.png" and "inverted.png" in file:
                image = Image.open("grayscale.png")
                WIDTH, HEIGHT = image.size
                return WIDTH, HEIGHT
            else:
                return 0, 0

# create inverted and grayscale versions of the original picture
# also provides support for JPEG and PNG files
def unpackElements(image_name):
    image = Image.open(image_name)
    WIDTH, HEIGHT = image.size
    maxsize = (300, 300)
    image.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    if image.mode == 'RGBA':
        try:
            try:
                raise RuntimeError
            except RuntimeError as err:
                err.message="RGBA is not yet supported!"
                raise
        except ValueError as e:
            print("An error occured: " + str(type(e)) + " " + e.message)
    else:
        inverted_image = PIL.ImageOps.invert(image)

        if image_name.endswith('jpeg') or image_name.endswith('jpg'):
            inverted_image.save('inverted.jpeg')
        elif image_name.endswith('png'):
            inverted_image.save('inverted.png')

        if image_name.endswith('jpeg') or image_name.endswith('jpg'):
            grayscale_image = Image.open(image_name).convert('L')
        elif image_name.endswith('png'):
            grayscale_image = Image.open(image_name).convert('LA')

        if image_name.endswith('jpeg') or image_name.endswith('jpg'):
            grayscale_image.save('grayscale.jpeg')
        elif image_name.endswith('png'):
            grayscale_image.save('grayscale.png')

    return WIDTH, HEIGHT

# flip the image shown
def callback(e):
    if e == False:
        img2 = ImageTk.PhotoImage(Image.open('grayscale.jpeg'))
    else:
        img2 = ImageTk.PhotoImage(Image.open('inverted.jpeg'))
    panel.configure(image=img2)
    panel.image = img2

# create the custom GUI frame
class Application(tk.Frame):
    current_image_grayscale = False
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.flip_image = tk.Button(self, text='Show Grayscale', command=self.show_grayscale)

        self.flip_image.pack(side='top')

        self.quitButton = tk.Button(self, text='Quit',
            fg='red', command=self.quit)

        self.quitButton.pack(side='bottom')

    def show_grayscale(self):
        if not self.current_image_grayscale:
            self.flip_image['text'] = 'Show Inverted'
        else:
            self.flip_image['text'] = 'Show Grayscale'

        callback(self.current_image_grayscale)

        self.current_image_grayscale = not self.current_image_grayscale

# --------SCRIPT----------

# check for supported file in directory
os.chdir("./")
file = glob.glob("*.jpeg")
img_name = ""

if file:
    img_name = [file_name for file_name in file if not file_name == 'grayscale.jpeg' or
                file_name == 'inverted.jpeg'][0]
else:
    file = glob.glob("*.jpg")
    if file:
        img_name = [file_name for file_name in file if not file_name == 'grayscale.jpg' or
                    file_name == 'inverted.jpg'][0]
    else:
        file = glob.glob("*.png")
        if file:
            img_name = [file_name for file_name in file if not file_name == 'grayscale.png' or
                        file_name == 'inverted.png'][0]
        else:
            print("File is either not found or not supported!")
            exit(-1)

WIDTH = 0
HEIGHT = 0

WIDTH, HEIGHT = checkForNecessaryElements()
if WIDTH and HEIGHT != 0:
    if img_name.endswith(".jpeg"):
        print("grayscale.jpeg and inverted.jpeg already detected.")
    elif img_name.endswith(".jpg"):
        print("grayscale.jpg and inverted.jpg already detected.")
    elif img_name.endswith(".png"):
        print("grayscale.png and inverted.png already detected.")
    else:
        print("File is either not found or not supported!")
        exit(-1)
else:
    WIDTH, HEIGHT = unpackElements(img_name)
    if img_name.endswith(".jpeg"):
        print("grayscale.jpeg and inverted.jpeg unpacked.")
    elif img_name.endswith(".jpg"):
        print("grayscale.jpg and inverted.jpg unpacked.")
    elif img_name.endswith(".png"):
        print("grayscale.png and inverted.png unpacked.")
    else:
        print("File is either not found or not supported!")
        exit(-1)

frame_size = str(WIDTH) + "x" + str(HEIGHT + 56)  # trial and error to remove whitespace

root = tk.Tk()
root.geometry(frame_size)
app = Application(master=root)
app.configure(background='grey')
app.master.title('AfterimageCreator')

if img_name.endswith(".jpeg"):
    path = "inverted.jpeg"
elif img_name.endswith(".jpg"):
    path = "inverted.jpg"
elif img_name.endswith(".png"):
    path = "inverted.png"
else:
    print("Couldn't load inverted file!")
    exit(-1)

img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(app, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

app.mainloop()
