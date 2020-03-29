#!/bin/env python
# This code created functions that will check the quality of data
#Data quality checks include large numbers -999 into NAN, range checks, and certain logic checks concerning temperature ranges
#created by Marissa Cubbage 3/18/2020

#import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    global DataDF
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
  
    
    # define and initialize the missing data dictionary
    global ReplacedValuesDF
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data", '2. Gross Error', '3. Swapped','4. Range Fail'], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""
    for i in range (0,len(DataDF)-1):
       for j in range(0,3):
           if DataDF.iloc[i,j] == -999:
               DataDF.iloc[i,j]= np.nan
   
    ReplacedValuesDF.iloc[0,0]=DataDF['Precip'].isna().sum()
    ReplacedValuesDF.iloc[0,1]=DataDF['Max Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,2]=DataDF['Min Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,3]=DataDF['Wind Speed'].isna().sum()


    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    #precip
    for i in range (0,len(DataDF)-1):
           if (DataDF.iloc[i,0]<0) or (DataDF.iloc[i,0]>25):
               DataDF.iloc[i,0]= np.nan
    #temperature
    for i in range (0,len(DataDF)-1):
           if DataDF.iloc[i,2]< (-25):
               DataDF.iloc[i,2]= np.nan
    
    for i in range (0,len(DataDF)-1):
           if DataDF.iloc[i,1]>35:
               DataDF.iloc[i,1]= np.nan
    #wind speed      
    for i in range (0,len(DataDF)-1):
           if (DataDF.iloc[i,3]<0) or (DataDF.iloc[i,3]>10):
               DataDF.iloc[i,3]= np.nan
               
    ReplacedValuesDF.iloc[1,0]=DataDF['Precip'].isna().sum()-ReplacedValuesDF.iloc[0,0]
    ReplacedValuesDF.iloc[1,1]=DataDF['Max Temp'].isna().sum()-ReplacedValuesDF.iloc[0,1]
    ReplacedValuesDF.iloc[1,2]=DataDF['Min Temp'].isna().sum()-ReplacedValuesDF.iloc[0,2]
    ReplacedValuesDF.iloc[1,3]=DataDF['Wind Speed'].isna().sum()-ReplacedValuesDF.iloc[0,3]
               
    return(DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    ReplacedValuesDF.iloc[2,1]=(DataDF['Min Temp']> DataDF['Max Temp']).sum()
    ReplacedValuesDF.iloc[2,2]=(DataDF['Min Temp']> DataDF['Max Temp']).sum()

    for i in range (0,len(DataDF)-1):
           if DataDF.iloc[i,1] < DataDF.iloc[i,2]:
               tmp=DataDF.iloc[i,2]
               DataDF.iloc[i,2]= DataDF.iloc[i,1]
               DataDF.iloc[i,1]=tmp
               
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here

    for i in range (0,len(DataDF)-1):
           if (DataDF.iloc[i,1]-DataDF.iloc[i,2])>25:
             DataDF.iloc[i,1]=np.nan
             DataDF.iloc[i,2]=np.nan
             
    ReplacedValuesDF.iloc[3,1]=DataDF['Max Temp'].isna().sum()-(ReplacedValuesDF.iloc[1,1]+ReplacedValuesDF.iloc[0,1])
    ReplacedValuesDF.iloc[3,2]=DataDF['Min Temp'].isna().sum()-(ReplacedValuesDF.iloc[1,2]+ReplacedValuesDF.iloc[0,2])


    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)

#read in data     
ReadData('DataQualityChecking.txt')



#check 01
Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )

#check 02
Check02_GrossErrors( DataDF, ReplacedValuesDF )

#Check 03
Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )

#check 04
Check04_TmaxTminRange( DataDF, ReplacedValuesDF )

#re-import original data 
colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
DataDF1 = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                     delimiter=r"\s+",parse_dates=[0])
DataDF1 = DataDF1.set_index('Date')

#scatterplots of variables before and after data quality checking 

plt.plot(DataDF.index, DataDF1['Precip'],'r*', label='Before Data Quality Check')
plt.plot(DataDF.index, DataDF['Precip'],'b*', label='After Data Quality Check')
plt.xlabel('Daily Time Series 1915-1916')
plt.ylabel('Precipitation')

plt.legend()
plt.savefig('Precip.png')
plt.close()


plt.plot(DataDF.index, DataDF1['Max Temp'],'r*', label='Before Data Quality Check')
plt.plot(DataDF.index, DataDF['Max Temp'],'b*', label='After Data Quality Check')
plt.xlabel('Daily Time Series 1915-1916')
plt.ylabel('Maximum Temperature')
plt.legend()
plt.savefig('Max Temp.png')
plt.close()

plt.plot(DataDF.index, DataDF1['Min Temp'],'r*', label='Before Data Quality Check')
plt.plot(DataDF.index, DataDF['Min Temp'],'b*', label='After Data Quality Check')
plt.xlabel('Daily Time Series 1915-1916')
plt.ylabel('Minimum Temperature')
plt.legend()
plt.savefig('Min Temp.png')
plt.close()


plt.plot(DataDF.index, DataDF1['Wind Speed'],'r*', label='Before Data Quality Check')
plt.plot(DataDF.index, DataDF['Wind Speed'],'b*', label='After Data Quality Check')
plt.xlabel('Daily Time Series 1915-1916')
plt.ylabel('Wind Speed')
plt.legend()
plt.savefig('WindSpeed.png')
plt.close()

#write txt tab delimted file that has data that is quality checked
DataDF.to_csv('After_Data_Quality_Checking.txt', sep='\t', index=False)

#write txttab delimited file with failes checks data
ReplacedValuesDF.to_csv('Failed_Checks.txt', sep='\t', index=False)
 