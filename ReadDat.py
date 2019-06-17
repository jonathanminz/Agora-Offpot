import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(11, 4)})

# This is a program to read and parse the FINO windspeed and wind direction data into a pandas data frame. 
#The data has comments denoted by '#'. 
#The header for columns is on line 5. 
#Data is tab delimited. 

# WINDSPEED DATA 

WindSpeed = pd.read_csv("C:\Users\jonat\Downloads\TxT\FINO1_WindSpeed_90m_20040101_20151231", header = 0, delimiter= '\t', comment='#')
# Date and time data in this txt file is a string
#new = WindSpeed["Time"].str.split(" ", n = 1, expand = True) # Here we split the date and time into 2 columns and store is as another list
#WindSpeed["Date"] = new[0] # Now we have made 2 separate columns for Date and Time 
#WindSpeed["Time"] = new[1]
#WindSpeed = WindSpeed[['Date','Time','Value','Minimum','Maximum','Deviation', 'Quality']]# Rearranging columns
WindSpeed['Time'] = pd.to_datetime(WindSpeed['Time'], format = '%Y-%m-%d %H:%M:%S') # Changing date from Strings to Datetime format
#WindSpeed.set_index('Time', inplace=True) #Setting Time as dataframe index 




# WIND DIRECTION DATA
WindDirection = pd.read_csv("C:\Users\jonat\Downloads\TxT\FINO1_WindDirection_90m_20040101_20151231", header = 0, delimiter= '\t', comment='#')
WindDirection['Time'] = pd.to_datetime(WindDirection['Time'], format = '%Y-%m-%d %H:%M:%S') # Changing date from Strings to Datetime format
#WindDirection.set_index('Time', inplace=True) #Setting Time as dataframe index 





# DATA MANIPULATION AND FILTERING
WindSpeed = WindSpeed[WindSpeed.Value != -999] # Assuming that Value is a good filter for identifying good data. Quality is another discriminant. If all -999 points are removed then 596868 points are left. 6% reduction in data.
WindDirection = WindDirection[WindDirection.Value != -999] #Removing all rows with -999 as value reduces the number of points to 594620 which is about a similar 6% reduction.
Ws_Wd_Merged = pd.merge(WindSpeed, WindDirection[['Time','Value']],on = 'Time') # Merging the 2 datasets into one single dataframe called Ws_Wd_Merged.
Ws_Wd_Merged.rename(columns={'Value_x':'Ws_Value', 'Value_y':'Wd_Value'}, inplace= True) # renaming columns
Ws_Wd_Merged.set_index('Time', inplace=True)

WindDirection_RAW = pd.read_csv("C:\Users\jonat\Downloads\TxT\FINO1_WindDirection_90m_20040101_20151231", header = 0, delimiter= '\t', comment='#')#Test
WindSpeed_RAW = pd.read_csv("C:\Users\jonat\Downloads\TxT\FINO1_WindSpeed_90m_20040101_20151231", header = 0, delimiter= '\t', comment='#')#Test
Ws_Wd_Merged_RAW = pd.merge(WindSpeed_RAW, WindDirection_RAW[['Time','Value']],on = 'Time')


#DATA PLOTS
#WindSpeed['Value'].plot(kind = 'hist', bins=100)
#WindDirection['Value'].plot(kind = 'hist', bins=100)


#For Diffrence
ds1 = set([tuple(line) for line in df1.values])
ds2 = set([tuple(line) for line in df2.values])
ds1.difference(ds2)
pd.DataFrame(list(ds1.difference(ds2)))