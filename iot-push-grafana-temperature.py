import time
import random
import requests

# InfluxDB configuration
INFLUXDB_URL = 'https://influx-prod-13-prod-us-east-0.grafana.net/api/v1/push/influx/write'  # Replace with your actual InfluxDB URL
USER_ID = '1590137'  # Replace with your actual user ID
TOKEN = ''  # Replace with your actual token

def generate_random_temperature():
    return random.uniform(18.0, 30.0)  # Adjust range as per your requirements

def push_temperature_to_influxdb(temperature):
    timestamp = int(time.time() * 1000000000)  # Convert to nanoseconds
    data = f'temperature,location=living_room value={temperature} {timestamp}'
    
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
        temperature = generate_random_temperature()
        push_temperature_to_influxdb(temperature)
        time.sleep(60)  # Wait for 1 second
