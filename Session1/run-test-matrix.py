
# coding: utf-8

# ### Importing Libraries

# In[1]:

from bibliopixel import *
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import LEDMatrix

import time


# ### Shell commands to reset spidev

# In[ ]:

from subprocess import call
call(["sudo", "chmod", "a+rw", "/dev/spidev0.0"])


# ### Initial setup

# In[ ]:


H = 10
W = 10
numLeds = H * W
driver=DriverLPD8806(numLeds, ChannelOrder.BRG)
led=LEDMatrix(driver, width = W, height = H)



# ### LED testing - ON/OFF
# 

# In[ ]:

led.fillRGB(0,0,0) # turns everything off
led.update()

for i in range (H):
    print ('Diagonal testing')
    led.set(i,i,(0,0,180))
    led.update()
    time.sleep(0.25)



# ### LED Character testing

# In[ ]:

led.fillRGB(0,0,0) # turns everything off
led.update()

##led.drawChar(x, y, c, color, bg, size) 
## x,y top left corner coordinates
## c - character in ASCII: ord('A') - gives ascii value of A
## color - rgb tuple
## bg - also rgb tuple
## size - factor to scale character. 8 x 5 is the base

text = 'Hello world '

for i in text: 
    led.drawChar(x = 1,y = 2, c = ord(i), color = (0,250,0), bg = (50,50,50), size = 1)
    print(i)
    time.sleep(0.25)


