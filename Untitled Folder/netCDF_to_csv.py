
# coding: utf-8

# ### Import libraries

# In[1]:

from netCDF4 import Dataset
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
import numpy.ma as ma


# ### Import datafile

# In[2]:

my_example_nc_file = '/Users/radharamachandran/Downloads/Data-Guatemala.nc'
fh = Dataset(my_example_nc_file, mode='r')


# ### Pick out the necessary variables

# In[3]:

time = fh.variables['time'][:]
y = fh.variables['yield'][:]
lon = fh.variables['lon'][:]
lat = fh.variables['lat'][:]


# ### Function that writes a variable to a csv file

# In[4]:

def write_to_csv(var_name, output_filename):
    with open(output_filename, "w", newline="") as csvFile:
        outputwriter = csv.writer(csvFile, delimiter=',')
        # yield has 5 levels of nesting, not for other variables
        
        if (np.size(var_name)>1000): ## Quick and dirty way to separate out 'yield' from other variables
            for var0 in var_name:
                for var1 in var0:
                    for var2 in var1:
                        for var3 in var2:
                            new_var = [0 if (x is np.ma.masked) else x for x in var3]
                            outputwriter.writerow(new_var)
                            
        else:
            outputwriter.writerow(var_name)


# ### Run function write_to_csv
# #### First argument is the variable name, second argument is the file name

# In[6]:

write_to_csv(y, 'guetamala-yield.csv')
write_to_csv(lat, 'guetemala-lat.csv')
write_to_csv(lon, 'guetemala-lon.csv')
write_to_csv(time, 'guetemala-time.csv')


# In[ ]:



