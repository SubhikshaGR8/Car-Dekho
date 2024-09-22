import pandas as pd

# Load the Excel file
df = pd.read_excel("Appended_Details.xlsx")


#<================================= Body Types ===================================>
df['BodyType'] = df['BodyType'].fillna('Minivans')  # Fill NaN with 'Minivan'
# Ensure 'BodyType' is of type string
df['BodyType'] = df['BodyType'].astype(str)
print("Filled NaN values with:", 'Minivans')





#<================================= Fuel Types ===================================>
df['FuelType'] = df['FuelType'].astype(str)





#<================================= Owner Number ===================================>
df['OwnerNumber'] = df['OwnerNumber'].astype(int)





#<================================= KM Driven ===================================>
df['KilometersDriven'] = df['KilometersDriven'].astype(str).str.replace(',', '').str.strip()
df['KilometersDriven'] = df['KilometersDriven'].astype(int)
# Impute zeros with the median of non-zero values
median_kms = df.loc[df['KilometersDriven'] > 0, 'KilometersDriven'].median()
df['KilometersDriven'] = df['KilometersDriven'].replace(0, median_kms)





#<================================= Transmission ===================================>
df['Transmission']=df['Transmission'].astype(str)




#<================================= BuiltCompany ===================================>
df[['BuiltCompany', 'model']] = df[['BuiltCompany', 'model']].apply(lambda x: x.str.strip().str.title())





#<================================= Price ===================================>
def clean_price(price):
    price = price.replace('₹', '').replace(',', '').strip()
    if 'Crore' in price:
        return int(float(price.replace('Crore', '').strip()) * 10000000)  # Convert Crore to integer
    elif 'Lakh' in price:
        return int(float(price.replace('Lakh', '').strip()) * 100000)  # Convert Lakh to integer
    else:
        return int(float(price))  # Handle regular integers
df['price'] = df['price'].astype(str).apply(clean_price)




#<================================= Mileage ===================================>
# 'Mileage' cleaning function
def clean_mileage(mileage):
    if isinstance(mileage, str):
        # Extract the numeric part using regex
        numeric_value = pd.Series(mileage).str.extract(r'(\d+\.?\d*)')[0]  # Extracts the first match
        return numeric_value.astype(float).iloc[0]  # Return as float
    return None  # Handle non-string entries
# Apply the cleaning function
df['Mileage'] = df['Mileage'].apply(clean_mileage)
# Fill missing values in 'Mileage' ---> using median imputation
df['Mileage'] = df['Mileage'].fillna(df['Mileage'].median())




#<================================= Max Power ===================================>
# 'Max Power' cleaning function
def clean_max_power(max_power):
    if isinstance(max_power, str):
        # Extract the numeric part using regex
        numeric_value = pd.Series(max_power).str.extract(r'(\d+\.?\d*)')[0]  # Extracts the first match
        return numeric_value.astype(float).iloc[0]  # Return as float
    return None  # Handle non-string entries
# Apply the cleaning function
df['Max Power'] = df['Max Power'].apply(clean_max_power)
# Fill missing values in 'Max Power' ---> using median imputation
df['Max Power'] = df['Max Power'].fillna(df['Max Power'].median())




#<================================= Torque ===================================>
# Convert Torque to numeric, coercing errors to NaN
df['Torque'] = pd.to_numeric(df['Torque'], errors='coerce')
# Calculate the median of the Torque column, excluding NaN values
median_torque = df['Torque'].median()
# Fill missing values in Torque with the median
df['Torque'] = df['Torque'].fillna(median_torque)





#<================================= Categorical Types ===================================>
# Handling missing values for categorical columns
categorical_columns = [ 'Engine Type', 'Steering Type']


#<================================= Engine Types ===================================>
df['Engine Type'] = df['Engine Type'].fillna('Not Available')




#<================================= Features ===================================>
df['Features'] = df['Features'].replace('Nan', 'Data Not Available')




#<================================= Steering Types ===================================>
# Step 2: Replace unwanted terms with 'Electric' and filter out rows
df['Steering Type'] = df['Steering Type'].replace({'electrical': 'Electric'}, regex=True)
df['Steering Type'] = df['Steering Type'].replace({'EPAS': 'Electric'}, regex=True)
df['Steering Type'] = df['Steering Type'].replace({'electric': 'Electric'}, regex=True)
df['Steering Type'] = df['Steering Type'].replace({'Electrical': 'Electric'}, regex=True)
df['Steering Type'] = df['Steering Type'].replace({'Electronic': 'Electric'}, regex=True)
df['Steering Type'] = df['Steering Type'].replace({'power': 'Power'}, regex=True)
df['Steering Type'].fillna(method='ffill', inplace=True)






#<================================= Engines ===================================>
def clean_engine(engine):
    if isinstance(engine, str):
        engine_value = engine.replace(' CC', '').strip()
        return int(engine_value) if engine_value.isdigit() else None
    return None  # Handle non-string entries
df['Engine'] = df['Engine'].apply(clean_engine)
df['Engine'] = df['Engine'].fillna(df['Engine'].median()).astype(int)  # Ensure it's an integer






#<================================= Top Speed ===================================>
# First, clean TopSpeed to ensure it's numeric
df['Top Speed'] = df['Top Speed'].astype(str).str.replace(' Kmph', '').str.replace(' kmph', '').str.replace('km/hr', '').str.replace(',', '').str.strip()
df['Top Speed'] = pd.to_numeric(df['Top Speed'], errors='coerce')  # Convert to numeric, coerce errors to NaN
df['Top Speed'] = df['Top Speed'].fillna(df['Top Speed'].median())  # Fill with median
df['Top Speed'] = df['Top Speed'].astype(int)




#<================================= Model year ===================================>
df['modelYear'] = df['modelYear'].astype(int)


#<================================= Car link & Features ===================================>
# df['CarLink'] = df['CarLink'].astype(str).str.strip()
# df['Features'] = df['Features'].astype(str).str.strip()
# df['Features'] = df['Features'].apply(lambda x: ', '.join([feature.strip().capitalize() for feature in x.split(',')]))






#<================================= Columns  ===================================>
# columns_to_keep = [
#     'City','BodyType','FuelType','Engine', 'Engine Type','Transmission','Mileage','OwnerNumber', 'KilometersDriven', 'BuiltCompany', 'model',  'Max Power', 'Torque', 'Steering Type', 'Top Speed', 'Features','CarLink', 'price'
# ]

columns_to_keep = [
    'City','BodyType','FuelType','Engine', 'Engine Type','Transmission','Mileage','OwnerNumber', 'KilometersDriven', 'BuiltCompany', 'model',  'Max Power', 'Torque', 'Steering Type', 'Top Speed','modelYear','price'
]





# Filter the DataFrame to keep only the desired columns
filtered_df = df[columns_to_keep]


# Save the updated DataFrame to a new Excel file
output_file_path = "cardekho_ds.xlsx"
filtered_df.to_excel(output_file_path, index=False)

print(f"Updated data has been saved to {output_file_path}")