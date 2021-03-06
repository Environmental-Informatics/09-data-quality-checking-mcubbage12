#!/bin/env python
# add your header here
#
import pandas as pd
import numpy as np

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
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
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
           if (DataDF['Precip']<=0) or (DataDF['Precip']>=25):
               DataDF.iloc[i,0]= np.nan
    #temperature
    for i in range (0,len(DataDF)-1):
           if DataDF['Min Temp']<= 25:
               DataDF.iloc[i,2]= np.nan
    
    for i in range (0,len(DataDF)-1):
           if DataDF['Max Temp']>=35:
               DataDF.iloc[i,1]= np.nan
               
    for i in range (0,len(DataDF)-1):
           if (DataDF['Precip']<=0) or (DataDF['Precip']>=25):
               DataDF.iloc[i,0]= np.nan
               
               
    return( DatCheck01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here

    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here

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
