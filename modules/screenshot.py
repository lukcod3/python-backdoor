import os
import time
import ImageGrab


# take a screenshot
def screenshot(server):
    img = ImageGrab.grab()
    filename = os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S') + '.png')
    img.save(filename)
    server.send('Screenshot saved as: ' + filename + '\n')
