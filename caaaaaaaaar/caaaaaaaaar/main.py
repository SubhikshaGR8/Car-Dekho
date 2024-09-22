import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define the list of cities and their corresponding Excel file names
cities = ['delhi', 'chennai', 'kolkata', 'jaipur',  'hyderabad', 'bangalore']
file_paths = [f'SourceData/{city}_cars.xlsx' for city in cities]

# Define the specific keys we want to extract from the 'new_car_specs' column
desired_keys = ['Mileage', 'Engine', 'max power', 'Torque', 'Seats']
desired_list_keys = ['drive type', 'steering type', 'Gear Box', 'Top Speed']

def extract_details(row, city):
    # Extracting necessary details from the 'new_car_detail' field
    try:
        details = eval(row['new_car_detail'])
    except KeyError:
        details = {}
        logging.warning(f"'new_car_detail' not found in row: {row}")

    fuel_type = details.get('ft', 'N/A')
    body_type = details.get('bt', 'N/A')
    kilometers = details.get('km', 'N/A')
    transmission = details.get('transmission', 'N/A')
    ownerNo = details.get('ownerNo', 'N/A')
    oem = details.get('oem', 'N/A')
    model = details.get('model', 'N/A')
    modelYear = details.get('modelYear', 'N/A')
    variant = details.get('variantName', 'N/A')
    price = details.get('price', 'N/A')

    # Extracting entire details from the 'new_car_specs' field
    specs = eval(row['new_car_specs']) if 'new_car_specs' in row else {}
    car_data = extract_car_specs(specs)

    # Extracting features from 'new_car_feature' field
    features = eval(row['new_car_feature']) if 'new_car_feature' in row else {}
    feature_list = [feature['value'] for feature in features.get('top', [])]

    return {
        'City': city,
        'FuelType': fuel_type,
        'BodyType': body_type,
        'KilometersDriven': kilometers,
        'Transmission': transmission,
        'OwnerNumber': ownerNo,
        'BuiltCompany': oem,
        'model': model,
        'modelYear': modelYear,
        'modelVariant': variant,
        **car_data,
        'CarLink': row.get('car_links', 'N/A'),
        'Features': ', '.join(feature_list),
        'price': price,
    }

# Function to extract all the key-value pair from new_car_specs field
def extract_car_specs(specs):
    extracted_data = {}
    for item in specs.get('top', []):
        extracted_data[item['key']] = item['value']
    for section in specs.get('data', []):
        for item in section.get('list', []):
            extracted_data[item['key']] = item['value']
    return extracted_data

# Process each file and save the structured data
for city, file_path in zip(cities, file_paths):
    df = pd.read_excel(file_path, engine='openpyxl')
    logging.debug(f'Processing file: {file_path}')
    logging.debug(f'Columns: {df.columns.tolist()}')

    # Apply the extraction function to the dataframe
    structured_data = df.apply(lambda row: extract_details(row, city), axis=1)
    structured_df = pd.DataFrame(structured_data.tolist())

    # Save the structured data to a new Excel file
    structured_df.to_excel(f'structured_{city}.xlsx', index=False)

print("Done!")
