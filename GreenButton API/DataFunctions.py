
# coding: utf-8

# In[2]:

import numpy as np
import csv
import time
import matplotlib
import matplotlib.pyplot as plt
import datetime
#import pandas as pd
#from LEDsetup import *


# ### Open datafiles

# In[31]:

def OpenData(filename):
    time_stamp = []
    value = []
    with open(filename) as f:
        cf = csv.DictReader(f, fieldnames=['time_stamp', 'value'])
        for row in cf:
            try:
                time_stamp.append(datetime.datetime.strptime(row['time_stamp'], "%Y-%m-%d"))
                
            except:
                time_stamp.append(datetime.datetime.strptime(row['time_stamp'], "%Y-%m-%d %H:%M:%S"))
            value.append(float(row['value']))
                
    
    return(time_stamp, value)


# ### Generating color scale

# In[19]:

#def ColorScale(steps, color1, color2):
    #clrs = []
    #inc = 1/(steps-1)
    #print(inc)
    
    #for i in range(steps):
        #new_color = (int(color1[0]*i*inc+color2[0]*(steps-i-1)*inc),
                     #int(color1[1]*i*inc+color2[1]*(steps-i-1)*inc), 
                     #int(color1[2]*i*inc+color2[2]*(steps-i-1)*inc))
        #print(new_color)
        #clrs.append(new_color)

        
    #return clrs



# In[22]:

def ColorScaler(color1, color2, value):
    min_value = min(value)
    max_value = max(value)
    clr_data = []
    
    for val in value:
        ratio = (val - min_value)/(max_value-min_value)
        new_color = (int(color2[0]*ratio+color1[0]*(1-ratio)),
                     int(color2[1]*ratio+color1[1]*(1-ratio)), 
                     int(color2[2]*ratio+color1[2]*(1-ratio)))
        print(new_color)
        clr_data.append(new_color)

        
    return clr_data


# In[23]:

clr_data = ColorScaler((0,255,0),(255,0,0), range(10))


# In[26]:

def NumScaler(led1, led2, value):
    min_value = min(value)
    max_value = max(value)
    num_data = []
    
    for val in value:
        ratio = (val - min_value)/(max_value-min_value)
        new_num = led1 + int((led2-led1)*ratio)
        print(new_num)
        num_data.append(new_num)

        
    return num_data


# In[27]:

num_data = NumScaler(0,39,range(10))


# In[28]:

def Flash(num_flashes, delay, color, led1 = 0, led2 = 79):
    for i in range(num_flashes):
        led.fill(color, led1, led2)
        led.update
        time.sleep(delay)
        


# In[ ]:

def Pulse(num_pulses, color, led1 = 0, led2 = 79):
    ## Step-up intensity by 10% increments, then step down by the same every 0.1 seconds. total time = 2 sec
    
    intensity = np.arange(0,1.1,0.1) 

    for i in intensity:
        color_new = (int(color[0]*i),int(color[1]*i),int(color[2]*i)) 
        # There is probably a more elegant way to do this.. 
        #print color_new
        led.fill(color_new, led1, led2)
        led.update()
        time.sleep(0.1)

    for i in reversed(intensity):
        color_new = (int(color[0]*i),int(color[1]*i),int(color[2]*i)) 
        #print color_new
        led.fill(color_new, led1, led2)
        led.update()
        time.sleep(0.1)        

