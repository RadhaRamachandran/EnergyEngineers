
# coding: utf-8

# In[1]:

from bibliopixel import *
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import LEDStrip
import bibliopixel.colors as colors
import csv
import numpy as np


# In[2]:

LedsPerSide = 8


# In[3]:

NumLeds= LedsPerSide*4*2 ##* 4 sides * 2 levels
driver=DriverLPD8806(NumLeds)
led=LEDStrip(driver)


# ### Import data

# In[3]:

clean_ratio = [] 
with open('Carbon_lbsperMW_monthly_average.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        clean_ratio.append(row)
        ## Column 1: Month
        ## Column 2: Lbs CO2 / MW of energy
        ## Column 3: Year


# ### Generating color scale

# In[4]:

red = 0
green = 255
stepSize = 25
color_gn_rd = []
color_gn_rd.append((green, red, 0)) ## the lights are GRB format


# In[5]:

while(red < 255): ## start with green and increase red
    red += stepSize;
    if(red > 245):
        red = 255; 
    color_gn_rd.append((green,red,0))

while(green > 0): ## start with red + green and decrease green
    green -= stepSize;
    if(green < 6):
        green = 0; 
    color_gn_rd.append((green,red,0)); 
    
color_gn_rd


# In[5]:

### from US Energy Information Agency Website: https://www.eia.gov/tools/faqs/faq.cfm?id=74&t=11
### Max value - 2170 for Lignite
### Min value - 1200 for natural gas
### Min value - 0 (renewables)
### for simplicity - let max and min be 0 and 2000 
### 23 color options ~~ changes every 100. 
### unfortunately all PJM data oscillates between 1400 and 1500
### Maybe we can change pulsing speed or number of lights displayed for the tens place

color_disp = []
ledON = []
for a,b,c in clean_ratio: 
    color_disp.append(np.floor(int(b)/100))
    ## 100's position represented by color bar --> going from green to red for 100 to 2000 ish
    
    ledON.append(np.floor(np.remainder(int(b),100) * LedsPerSide/100))
    
    ## 0 - 100 scaled by the number of lamps on each side
    ## x is the user-defined number of Led's per side


# ### Display yearly WattTime data

# In[9]:

DisplaySide = 1 # Set the side on which the data will be displayed here.
FirstLed_bottom = LedsPerSide*(DisplaySide-1)+1
FinalLed_bottom = LedsPerSide*DisplaySide

FirstLed_top = LedsPerSide*(DisplaySide + 4 -1)+1
FinalLed_bottom = LedsPerSide*(DisplaySide + 4 -1)+1


# In[10]:

def led_set(start_position, TotalLEDs, color):
    led.fill(color, start=start_position,end=start_position+numLEDs)
    led.update()
    return


# In[11]:

print ('Starting Display')
print ('Press \'control + c\' to stop' )

year = 2014
months = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


# In[ ]:

led.fill((0,0,0),start=FirstLed_bottom, end=FinalLed_bottom)
led.update()

#Turn all lights off Top    
led.fill((0,0,0),start=FirstLed_top, end=FinalLed_top)
led.update()
while True: 
    for i, month in enumerate(months):
        print month, year

        #Set bottom panel
        led_set(ledFirst_bottom, ledON[i], color_disp[i]) 
        #ledON gives the number of LED's that will be turned on
        #color_disp specifies color

        #Set top panel
        led_set(ledFirst_bottom + 2*int(i/3), 2, (200,150,100))
       

        time.sleep(2.)
        

