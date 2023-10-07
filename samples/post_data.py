import csv
import requests

ENDPOINT = "localhost:1026"

# Open the CSV file for reading
with open('sample_dataset.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Get the column names from the CSV header
    column_names = csv_reader.fieldnames

    # Iterate through each row in the CSV
    for row in csv_reader:
        # Prepare the data along with column names
        aux_data = {}
        for column_name in column_names:
            aux_data = row[column_name]
            # Make a POST request to the API
            api_url = f'http://{ENDPOINT}/v2/entities/urn:ngsi-ld:entity:a7f63730-43c7-4a6b-93c1-8b8903e76dc1/attrs/{column_name}/value'
            headers = {'fiware-service': 'smart', 'fiware-servicepath':'/', 'Content-Type':'text/plain'}  # Add any required headers

            print(f'PUT Topic: {api_url} - PAYLOAD: {aux_data}')

            response = requests.put(api_url, data=aux_data, headers=headers)

            print(f'{response.status_code} {response.text}')

        # Handle the API response (e.g., print response status code)
        #print(f"Row {row['id']} - Status Code: {response.status_code}")

        # Optionally, you can handle errors and log them here
        #if response.status_code != 200:
        #    print(f"Error for Row {row['id']}: {response.text}")
