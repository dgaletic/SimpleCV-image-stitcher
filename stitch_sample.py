import SimpleCV
import os
import time
from numpy import vstack,hstack

c = SimpleCV.Camera()

# Without this 0.5 sec sleep, the first image my camera takes is very dark, 
# I suppose the issue is it not calibrating fast enough after turning on?
# time.sleep(0.5)

matrices = []

for i in range(10):
    img = c.getImage()
    matrices.append(img.getNumpy())
    time.sleep(0.5)

mat = vstack(matrices)
img_stitched = SimpleCV.Image(mat)
img_stitched.save("stitched_h.png")

mat = hstack(matrices)
img_stitched = SimpleCV.Image(mat)
img_stitched.save("stitched_v.png")

print "Images saved in", os.getcwd()
