
# coding: utf-8

# In[2]:

import requests
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize
import time


# In[2]:

from bibliopixel import *
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import LEDStrip
import bibliopixel.colors as colors


# ## Set up LED Strip

# In[3]:

print("Welcome to SmartLamp Setup!\n")
x = input("Please set the number of LEDs on each side of your lamp: ")


# In[4]:

numLeds=x*4*2 ##x/side * 4 sides * 2 levels
driver=DriverLPD8806(numLeds)
led=LEDStrip(driver)


# #### NOTE: If you are reading from a CSV file instead of quering server, go directly to 'Read from CSV file' and ignore all steps from here to 'Write to CSV file'
# 
# ###Define Query
# 

# In[4]:

print 'Please enter the start date of the data you would like to access (format: yyyy-mm-dd)'
print 'For example: to start on January 12 2015, please enter 2015-01-12.'
start_date = raw_input ('Enter start date here: ')


# In[5]:

print 'Please enter the end date of the data you would like to access (format: yyyy-mm-dd)'
end_date = raw_input ('Enter end date here: ')


# In[6]:

ba = 'PJM' # Balancing Authority
start_at= start_date
end_at=end_date
url = 'https://api.watttime.org:443/api/v1/datapoints/?ba='+ba+'&start_at='+start_at+'&end_at='+end_at
#url = 'https://api.watttime.org:443/api/v1/datapoints/?ba=PJM&start_at=2015-11-19T11%3A30%3A00&end_at=2015-11-19T12%3A00%3A00'


# In[7]:

url


# ###Query WattTime

# In[10]:

r = requests.get(url, headers={'Authorization': 'Token a21f7ed01b6effc9a9aee1d02b6276d67bbbf851'})
data = r.json()
df=json_normalize(data[u'results'],'genmix',['timestamp','carbon','ba','created_at','market','freq'])
#df
data[u'count']

#### The query only returns one page. We need to loop the query to get all data. 



# In[11]:

### Query through all pages & writing to dataframe
#### Takes a while

while True:
    try: 
        url = data[u'next']
        r = requests.get(url, headers={'Authorization': 'Token a21f7ed01b6effc9a9aee1d02b6276d67bbbf851'})
        data_2 = r.json()
        df_2 = json_normalize(data_2[u'results'],'genmix',['timestamp','carbon','ba','created_at','market','freq'])
        df = df.append(df_2)
        data = data_2
   
    except:
        break


# ### Calculating % Carbon Emissions by month

# In[12]:

## Total carbon
df['total_carbon'] = df['carbon']*df['gen_MW']
df


# ###Sorting Dataframe by Month

# In[13]:

df['year'] = pd.DatetimeIndex(df['timestamp']).year
df['month'] = pd.DatetimeIndex(df['timestamp']).month


# ### Write to CSV file

# In[ ]:

df.to_csv('WattTime_1year_2014.csv', sep=',')


# ### Read from CSV 
# #### Do this if you have already downloaded from server

# In[ ]:

#df = pd.read_csv('WattTime_1year_2014.csv', index_col=0, parse_dates=True)


# In[ ]:

df_monthly = df.groupby(['month', 'year'])
monthly_total_genMW = df_monthly['gen_MW'].sum()
monthly_total_carbon = df_monthly['total_carbon'].sum()


# ### Calculating % carbon

# In[14]:

clean_ratio = monthly_total_carbon.divide(monthly_total_genMW)
clean_ratio


# ### Generating color scale

# In[15]:

red = 0
green = 255
stepSize = 25
color_gn_rd = []
color_gn_rd.append((green, red, 0)) ## the lights are GRB format


# In[17]:

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


# ### Applying color scale

# In[18]:

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
for j in clean_ratio: 
    color_disp.append(np.floor(j/100))
    ## 100's position represented by color bar --> going from green to red for 100 to 2000 ish
    
    ledON.append(np.floor(np.remainder(j,100) * x/100))
    
    ## 0 - 100 scaled by the number of lamps on each side
    ## x is the user-defined number of Led's per side


# ### Display yearly WattTime data

# In[19]:

while True: 
    print ('Please set the side on which the WattTime data will be displayed. Enter 1, 2, 3 or 4')

    try:
        side_number = int(raw_input('Side number (1,2,3 or 4): '))
        if ((side_number > 0) & (side_number < 5)): 
            ledFirst_bottom = x*(side_number-1)+1
            ledFinal_bottom = x*side_number
            
            ledFirst_top = x*(side_number + 4 -1)+1
            ledFinal_bottom = x*(side_number + 4 -1)+1
            break
            
        else:
            print ('Not a valid number! Try again.')
        
    except:
        print('Not a valid entry! Try again.')


# In[20]:

## x = number of LED per side of the cube - user defined. 
## numLEDS = number of LEDs to be turned on
## start_position = for the LED's to be turned on
## color=GRB color

def led_set(start_position, numLEDs, color):
    led.fill(color, start=start_position,end=start_position+numLEDs)
    led.update()
    return


# ###WattTime Carbon Intensity Yearly Display

# In[21]:

print ('Starting Display')
print ('Press \'control + c\' to stop' )

year = 2014
months = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    


# In[24]:

while True: 
    for i, month in enumerate(months):
        print month, year

        #Turn all lights off Bottom 
        led.fill((0,0,0),start=ledFirst_bottom, end=ledLast_bottom)
        led.update()

        #Turn all lights off Top    
        led.fill((0,0,0),start=ledFirst_top, end=ledLast_top)
        led.update()

        #Set bottom panel
        led_set(ledFirst_bottom, ledON[i], color_disp[i])

        #Set top panel
        led_set(ledFirst_bottom + 2*int(i/3), 2, (200,150,100))

        time.sleep(1.)
        

