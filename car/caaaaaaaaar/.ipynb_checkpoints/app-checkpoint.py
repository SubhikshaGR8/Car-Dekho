import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import sklearn

col1, col2, col3 = st.columns(3)

# Load the saved model
model, version = joblib.load('rforest_model.joblib')

# Load the scaler
scaler = joblib.load('scaler.joblib')

# Load the label encoders
with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)


#Data model load check
if sklearn.__version__ != version:
    st.error(f"Model was trained with scikit-learn version {version}, but you're using {sklearn.__version__}.")
else:
    # Continue with prediction
    st.write("Model loaded successfully!")




#Display the app title
st.title('Know your car price !')


# Create input fields for the category features
with col1:
    city = st.selectbox('City', ['bangalore', 'chennai', 'hyderabad','delhi','jaipur','kolkata'])

with col2:
    body_type = st.selectbox('BodyType',['Hatchback','SUV','Sedan','MUV','Coupe','Minivans','Pickup Trucks','Convertibles','Hybrids','Wagon'])


with col3:
    fuel_type = st.selectbox('FuelType', ['Petrol','Diesel','Lpg','Cng','Electric'])


with col1:
    transmission = st.selectbox('Transmission', ['Manual', 'Automatic'])
with col2:
    built_company = st.selectbox('BuiltCompany', ['Maruti','Ford','Tata','Hyundai','Jeep','Datsun','Honda','Mahindra','Mercedes-Benz','Bmw','Renault','Audi','Toyota','Mini','Kia','Skoda','Volkswagen','Volvo','Mg','Nissan','Fiat','Mahindra Ssangyong','Mitsubishi','Jaguar','Land Rover','Chevrolet','Citroen','Opel','Mahindra Renault','Isuzu','Lexus','Porsche','Hindustan','Motors'])
with col3:
    steering_type = st.selectbox('Steering Type', ['Power','Electric','Manual','Hydraulic'])

# Create input fields for the Numerical features
with col1:
    engine_capacity = st.number_input('Engine', min_value=0, max_value=5000, value=0)
with col2:
    Fuel_Mileage = st.number_input('Mileage', min_value=7, max_value=141, value=7)
with col3:
    Owner_Number = st.number_input('OwnerNumber', min_value=1, max_value=5, value=1)

with col1:
    Kilometers_Driven = st.number_input('KilometersDriven', min_value=100, max_value=5600000, value=100)
with col3:
    model_year = st.number_input('modelYear', min_value=1985, max_value=2024, value=2024)




# Prepare the input for prediction
input_data = pd.DataFrame({
    'City': [city],
    'BodyType': [body_type],
    'FuelType': [fuel_type],
    'Transmission': [transmission],
    'BuiltCompany': [built_company],
    'Steering Type': [steering_type],
    'Engine': [engine_capacity],
    'Mileage': [Fuel_Mileage],
    'OwnerNumber': [Owner_Number],
    'KilometersDriven': [Kilometers_Driven],
    'modelYear': [model_year]
})

# Ensure that City is a string
city = str(city)


# Ensure all categorical values are within the LabelEncoder classes
def transform_or_error(col, value, encoder):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        st.error(f"Error: {value} in {col} is not recognized. Please choose a valid option.")
        return None


# Transform categorical inputs or show an error
valid = True
for col in ['City', 'BodyType', 'FuelType', 'Transmission', 'BuiltCompany', 'Steering Type']:
    transformed_value = transform_or_error(col, input_data[col][0], label_encoders[col])
    if transformed_value is None:
        valid = False  # Mark input as invalid
    else:
        input_data[col] = transformed_value


# If all inputs are valid, continue to prediction
if valid:
    # Define the numerical columns
    numerical_columns = ['Engine', 'Mileage','OwnerNumber', 'KilometersDriven', 'modelYear']

    # Apply scaling to the numerical inputs
    input_data[numerical_columns] = scaler.transform(input_data[numerical_columns])

    # Predict the price
    if st.button('Predict Price'):
        prediction = model.predict(input_data)
        st.write(f'Estimated Price: ₹{prediction[0]:,.2f}')