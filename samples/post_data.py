import csv
import json
import requests

ENDPOINT = "localhost:1026"

# Open the CSV file for reading
with open('sample_dataset.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Get the column names from the CSV header
    column_names = csv_reader.fieldnames
    # Iterate through each row in the CSV
    for row in csv_reader:
        try:
            # Prepare the data along with column names
            put_dict = {}

            aux_data = {}
            for column_name in column_names:
                if((len(column_name) < 2) or (column_name == "date")):
                    continue
                
                put_dict[column_name] = {"value": float(row[column_name]), "type":"float"}
                # Make a POST request to the API
                #put_list.append(aux_data)

            api_url = f'http://{ENDPOINT}/v2/entities/urn:ngsi-ld:entity:a7f63730-43c7-4a6b-93c1-8b8903e76dc1/attrs'
            headers = {'fiware-service': 'smart', 'fiware-servicepath':'/', 'Content-Type':'application/json'}  # Add any required headers

            put_payload = json.dumps(put_dict)
            print(f'PUT Topic: {api_url} - PAYLOAD: {put_payload}')

            response = requests.put(api_url, data=put_payload, headers=headers)

            print(f'{response.status_code} {response.text}')


        except:
            pass
        
        # Handle the API response (e.g., print response status code)
        #print(f"Row {row['id']} - Status Code: {response.status_code}")

        # Optionally, you can handle errors and log them here
        #if response.status_code != 200:
        #    print(f"Error for Row {row['id']}: {response.text}")
