
# importing the required modules
import glob #The glob module finds all the pathnames matching a specified pattern
import pandas as pd

# specifying the path to csv files
path = "D:/car_dekho_final/stru"

# csv or xlsx files in the path
file_list = glob.glob(path + "/*.xlsx")

# Create a list, to save the excel file's data, we want to merge.
excl_list = []

for file in file_list:
    # pd.read_excel(file_path) reads the excel
    excl_list.append(pd.read_excel(file))
 
# concatenate all DataFrames in the list into a single DataFrame, returns new DataFrame.
excl_merged = pd.concat(excl_list, ignore_index=True)
 
# exports the dataframe into excel file with specified name.
excl_merged.to_excel('Appended_Details.xlsx', index=False)