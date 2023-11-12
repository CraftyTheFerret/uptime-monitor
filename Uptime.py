import requests
import time

def endpoint_check(url):
    try:
        response = requests.get(url)
        # Corrected the comparison operator to '=='
        if response.status_code // 100 == 2:
            print(f"Endpoint {url} is_up.")
            # Return True and the status code when the endpoint is up
            return True, response.status_code
        else:
            print(f"Endpoint {url} is down. Status Code: {response.status_code}")
            return False, response.status_code
    except requests.exceptions.RequestException as e:
        # Handling any request exceptions
        print(f"Error checking {url}: {e}")
        return False, 0
    except requests.exceptions.ConnectionError:
        # Handling connection errors
        print(f"Connection error occurred with {url}.")
        return False, 0

endpoints = ["https://38.d.itsby.design/qbittorrent/", "https://gmail.com"]

def monitor_endpoints(endpoints):
    sleep_duration = 60
    while True:
        for url in endpoints:
            is_up, status_code = endpoint_check(url)  # Add this line
            if not is_up:
                with open('status_log.txt', 'w') as f:
                    f.write(f"Endpoint {url} is down. Status Code: {status_code}")
                    time.sleep(sleep_duration)
                if status_code == 401:
                    print(f"Endpoint {url} is partially down. Status Code: {status_code}")
                    time.sleep(sleep_duration)
                elif status_code != 200:
                    print(f"Endpoint {url} is down. Status Code: {status_code}")
                    time.sleep(sleep_duration)
                    sleep_duration += 60 # Incrementing the sleep duration by 60 seconds
                else:
                    print(f"Endpoint {url} is up. Status Code: {status_code}")
                    sleep_duration = 60 # Resetting the sleep duration to 60 seconds
monitor_endpoints(endpoints)
