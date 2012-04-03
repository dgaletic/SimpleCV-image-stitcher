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

    def tick(self):
        import copy # Workaround for dl.clear() issue
        self.dl_copy = copy.copy(self.dl[0]) # Workaround for dl.clear() issue

        self.time_left = self.time
        width = self.dl[0].width 
        height = self.dl[0].height
        while self.time_left:
            self.dl[0].text(str(self.time_left), (width / 2, height / 2))
            self.time_left -= 1
            time.sleep(1)
            # FIXME: dl.clear() causes
            # AttributeError: DrawingLayer instance has no attribute '_mImage'
            # self.dl.clear()

            # Is it cheaper to do this or create new drawing layers?
            # Probably the layers.
            # TODO: mutex lock.
            self.dl[0] = copy.copy(self.dl_copy) 
            # mutex release
                
    def set_drawing_layer(self, drawing_layer):
        self.dl = drawing_layer

    def get_drawing_layer(self):
        return self.dl


# main thread

cam = SimpleCV.Camera()
disp = Display.Display()

timer = Timer()
timer.daemon = True
timer.set_time(10)

img = cam.getImage()
text_layer = [img.dl()] # [] is a workaround for dl.clear()
timer.set_drawing_layer(text_layer)
timer.start()

while not disp.isDone():
    if disp.mouseLeft:
        break
    img = cam.getImage()
    if not thread.isAlive():
        img.clearLayers()
        img.addDrawingLayer(text_layer[0])
        dl = img.dl()
        timer.set_drawing_layer([dl])
    # else, it will just redraw the old value
    img.show()
    

quit()
