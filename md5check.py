#! /usr/bin/env python3
import pandas as pd

# create an md5.chk file, in the same folder 
# as the scenario data using 'md5sum compress* > md5.chk' 

# read md5.chk into dataframe
file = pd.read_csv('md5.chk',sep = " ", header = None)
file.columns = ['md5_MPI','Del','NOWF_Filename']
print('Saving check file to dataframe...')
file.drop(columns = ['Del'])
print('Printing Pandas output....')
print(file)

# write file as csv
print('Writing dataframe to csv.....') 
file.to_csv('md5chk_MPI.csv')
print('File saved')

