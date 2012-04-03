# Camera timer

import SimpleCV
from SimpleCV import Display
import threading
import time # Should be in the Timer class

class Timer(threading.Thread):
    def run(self):
        # "global name time not defined"; why?
        # import time 
        self.tick()

    def __init__(self, time = 5):
        threading.Thread.__init__(self)
        self.time = time

    def set_time(self, time):
        self.time = time

    def set_starting_image(self, image):
        self.img = image

    def set_drawing_layer(self, drawing_layer):
        self.dl = drawing_layer

    def get_drawing_layer(self):
        return self.dl

    def tick(self):

        self.time_left = self.time
        width = self.dl[0].width 
        height = self.dl[0].height
        while self.time_left:
            # create new layer
            layer_id = self.img.addDrawingLayer()
            new_dl = self.img.dl()
            # draw into it
            new_dl.text(str(self.time_left), (width / 2, height / 2))
            # But we don't actually want it to display text on the 
            # self.img image, that image is just to fetch the settings.

            # TODO
            # mutex lock.
            self.dl[0] = new_dl
            # mutex release

            self.time_left -= 1
            time.sleep(1)

            ## FIXME: dl.clear() causes
            ## AttributeError: DrawingLayer instance has no attribute '_mImage'
            ## self.dl.clear()
    

           
                


# main thread

cam = SimpleCV.Camera()
disp = Display.Display()

timer = Timer()
timer.daemon = True
timer.set_time(5)

img = cam.getImage()
timer.set_starting_image(img)

# [] is a workaround for dl.clear()
text_layer = [img.dl()] 
timer.set_drawing_layer(text_layer)

timer.start()

while timer.is_alive():
    img = cam.getImage()
    # TODO
    # if mutex not locked:
    img.clearLayers()
    img.addDrawingLayer(text_layer[0])
    # else, make it redraw the old value
    img.show()
img = cam.getImage()
img.save("/home/dgaletic/cheese.png")
