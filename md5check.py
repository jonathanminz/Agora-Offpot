#! /usr/bin/env python3
import pandas as pd

file = pd.read_csv('md5.chk',sep = " ", header = None)
file.columns = ['md5_MPI','Del','NOWF_Filename']
print('Saving check file to dataframe...')
file.drop(columns = ['Del'])
print('Printing Pandas output....')
print(file)
print('Writing dataframe to csv.....') 
file.to_csv('md5chk_MPI.csv')
print('File saved')

