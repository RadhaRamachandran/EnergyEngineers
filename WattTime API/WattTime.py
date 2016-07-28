
# coding: utf-8

# In[38]:

import requests
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import time


# In[ ]:

from bibliopixel import *
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import LEDStrip
from bibliopixel.colors import colors


# ## Set up LED Strip

# In[ ]:

numLeds=26
driver=DriverLPD8806(numLeds)
led=LEDStrip(driver)


# #### There are 6 LEDs per side of the cube

# In[ ]:

numLED=6


# ###LED SET

# In[ ]:

## numLED=number of LED's per side of the cube
## ledStart=index of first LED on that side of the cube
## color=GRB color
## ledon=number of LEDs to turn on 
def led_set(ledon, numLED, ledStart, color):
    led.fill(color,start=ledStart,end=ledon)
    led.fill(0,0,0),start=ledon,end=ledStart+numLED)
    led.update()
    return


# ###Define Query

# In[3]:

ba = 'PJM' # Balancing Authority
start_at='2015-11-20T11%3A30%3A00'
end_at='2015-11-20T12%3A30%3A00'
url = 'https://api.watttime.org:443/api/v1/datapoints/?ba=PJM&start_at='+start_at+'&end_at='+end_at
#url = 'https://api.watttime.org:443/api/v1/datapoints/?ba=PJM&start_at=2015-11-19T11%3A30%3A00&end_at=2015-11-19T12%3A00%3A00'


# ###Query WattTime

# In[4]:

r = requests.get(url)
data = r.json()


# ###JSON-->Pandas

# In[4]:

##quick look at the data format

#print (data[u'results'][0]['genmix'])
#print (data)


# In[5]:

##basic json -->pandas (using reformatted one below)

#df=json_normalize(data[u'results'])
#df2=json_normalize(data[u'results'][0]['genmix'])
#df


# ### Cleaning up and merging the dataframe

# In[5]:

df=json_normalize(data[u'results'],'genmix',['timestamp','carbon','ba','created_at','market','freq'])
df


# ###Calculate Generation Totals

# In[6]:

fuel=df.groupby(['timestamp'])
fuel_total=fuel.sum()
fuel_total


# ####some summary statistics

# In[40]:

tot=fuel_total['gen_MW'].sum()
fmax=fuel_total['gen_MW'].max()
fmin=fuel_total['gen_MW'].min()
fmean=fuel_total['gen_MW'].mean()
finc=(fmax-fmin)/numLED

tot,fmax,fmin,fmean,finc


# In[47]:

color=(0,0,155) #blue
##bscale=[(255,255,204),(255,237,160),(254,217,118),(254,178,76),(253,141,60),
## (252,78,42),(227,26,28),(189,0,38),(128,0,38)] #9 colors in white to red


# ###Simple Flash

# In[43]:

### Very simple flash function.  
## - takes range of values from query
## - divides into 6 bins (for 6 leds)
## - turns on the first N leds depending on the generation total for this entry


# In[44]:

for index,row in fuel_total.iterrows():
    #print((row['gen_MW']-fmin)/finc)
    val=row['gen_MW']-fmin
    if val < finc :
        ledon=0
    if finc <= val < 2*finc :
        ledon=1
    if finc*2 <= val < 3*finc :
        ledon=2 
    if finc*3 <= val < 4*finc :
        ledon=3 
    if finc*4 <= val < 5*finc :
        ledon=4 
    if finc*5 <= val < 6*finc :
        ledon=5 
    #print('LED',ledon)
    #led_set(ledon, numLED, 0, color) 
    time.sleep(1.)
        
    


# ###Save as CSV

# In[46]:

df.to_csv('WattTimeTest.csv', sep=',')

