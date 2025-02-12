import time
import random
import requests
from requests.auth import HTTPBasicAuth
import json

# InfluxDB configuration
INFLUXDB_URL = 'https://influx-prod-13-prod-us-east-0.grafana.net/api/v1/push/influx/write'  # Replace with your actual InfluxDB URL
USER_ID = '1590137'  # Replace with your actual user ID
TOKEN = ''  # Replace with your actual token

# Example usage
url = "https://8af3-190-150-164-10.ngrok-free.app/api/v1/instruments/3/values"  # Replace with the actual URL
username = "api_user"
password = "apiUser123$"
data = {}  # Replace with the actual data you need to send

def generate_random_temperature():
    return random.uniform(18.0, 30.0)  # Adjust range as per your requirements


def post_request_with_basic_auth(url, username, password, data):
    # Perform the GET request with basic authentication
    response = requests.get(url, auth=HTTPBasicAuth(username, password),verify=False)
    temperature_value = None
    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        
        # Parse the JSON response
        status = response_json.get("status")
        results_qty = response_json.get("resultsQty")
        results = response_json.get("results", [])
        
        print(f"Status: {status}")
        print(f"Results Quantity: {results_qty}")
        print("Results:")

        for result in results:
            code = result.get("code")
            print(f"  Code: {code}")
            if code=='Temperature':
                values = result.get("values", [])
                print("  Values:")

                for value in values:
                    value_data = value.get("value")
                    decimal_places = value.get("decimalPlaces")
                    measurement_unity_id = value.get("measurementUnityId")
                    measurement_unity = value.get("measurementUnity")

                    print(f"    Value: {value_data}")
                    print(f"    Decimal Places: {decimal_places}")
                    print(f"    Measurement Unity ID: {measurement_unity_id}")
                    print(f"    Measurement Unity: {measurement_unity}")
                    temperature_value = value_data
    else:
        print(f"Request failed with status code: {response.status_code}")
    
    return temperature_value
    
def union_to_float(int_num, decimal_num):
    
    # Add the numbers together
    result = int_num + decimal_num
    
    # Convert the result to float (optional, since result will already be float)
    result_float = float(result)
    
    return result_float

def push_temperature_to_influxdb(temperature):
    timestamp = int(time.time() * 1000000000)  # Convert to nanoseconds
    data = f'temperature,location=kontein_room value={temperature} {timestamp}'
    
    headers = {
        'Content-Type': 'text/plain'
    }
    
    response = requests.post(INFLUXDB_URL, headers=headers, data=data, auth=(USER_ID, TOKEN))
    
    if response.status_code != 204:
        print(f"Error pushing to InfluxDB: {response.status_code} - {response.text}")
    else:
        print(f"Pushed temperature: {temperature}")

if __name__ == "__main__":
    while True:
        #temperature = generate_random_temperature()
        temperature = post_request_with_basic_auth(url, username, password, data)
        push_temperature_to_influxdb(temperature)
        time.sleep(30)  # Wait for 1 second
