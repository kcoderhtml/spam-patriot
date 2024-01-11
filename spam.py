import random
import requests
import string
import threading
import time
import signal
import socks
import socket

from faker import Faker

fake = Faker()

# pull proxies from socks5_proxies.txt

print("Loading proxies...")
with open('socks5_proxies.txt') as f:
    proxies = f.readlines()
    prox_addresses_full = [x.strip() for x in proxies]
    proxy_addresses = [{'address': prx.split(':')[0], 'port': prx.split(':')[1]} for prx in prox_addresses_full]
print("Loaded " + str(len(proxy_addresses)) + " proxies")

url = 'https://www.hhposall.xyz/php/app/index/verify-info.php?t='

headers = {
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.usavdfaadf.xyz/',
    'sec-ch-ua-platform': '"macOS"'
}


def randomProxy():
    """
    Returns a random proxy from the list of proxies.

    Returns:
        dict: A dictionary containing the proxy address and port.
    """
    return random.choice(proxy_addresses)


# Generate random data
def getRandom():
    """
    Generate random data for testing purposes.

    Returns:
        dict: A dictionary containing random data fields such as 'murmur', 'uid', 'first_name', 'last_name', 'phone', 'email', 'address', 'city', 'zip', and 'state'.
    """
    random_data = {
        'murmur': ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
        'uid': str(random.randint(1, 100000)),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
        'address': fake.address(),
        'city': fake.city(),
        'zip': fake.zipcode(),
        'state': fake.state_abbr()  # You can modify this according to your needs
    }
    return random_data

def sendRequest():
    """
    Sends a request to the specified URL with a random number appended to it.
    Uses random data obtained from the getRandom() function.
    Prints the response text received from the server.
    """
    # Set up the SOCKS proxy to route through a public SOCKS5 proxy
    proxy = randomProxy()
    socks.set_default_proxy(socks.SOCKS5, proxy['address'], int(proxy['port']))
    socket.socket = socks.socksocket

    urlwithnum = url + str(random.randint(1000000000000, 9999999999999))
    random_data = getRandom()
    try:
        response = requests.post(urlwithnum, headers=headers, data=random_data)
    except requests.exceptions.ConnectionError:
        print("Connection Error, skipping request")
        # remove proxy from list, it's probably dead.
    print(response.text)


def spamRequests(num_requests, infinite, cooldown, cooldown2):
    """
    Sends a specified number of requests or runs in infinite mode, spamming requests indefinitely.

    Args:
        num_requests (int): The number of requests to send. If less than 100, it will be set to 100.
        infinite (bool): Flag indicating whether to run in infinite mode or not.
        cooldown (float): The cooldown time between each request in seconds.
        cooldown2 (float): The cooldown time between each batch of requests in seconds.

    Returns:
        None
    """
    if num_requests < 100:
        print("Minimum number of requests is 100")
        print("Setting number of requests to 100")
        num_requests = 100
    elif infinite == True:
        print("Indefinite Mode Activated")
        print("Cooldown between requests: " + str(cooldown) + " seconds")
        print("Press CTRL + C to stop")
        while True:
            if stop_flag:
                break
            for _ in range(100):
                if stop_flag:
                    break
                thread = threading.Thread(target=sendRequest)
                thread.start()
                threads.append(thread)
                thread.join()
                time.sleep(cooldown)
            time.sleep(cooldown2)
    else:
        print("Spamming " + str(num_requests) + " requests")
        print("Cooldown between requests: " + str(cooldown) + " seconds")
        for _ in range(int(num_requests / 100)):
            if stop_flag:
                break
            for _ in range(100):
                if stop_flag:
                    break
                thread = threading.Thread(target=sendRequest)
                thread.start()
                threads.append(thread)
                time.sleep(cooldown)
            time.sleep(cooldown2)
        for thread in threads:
            thread.join()


def signal_handler(signal, frame):
    """
    Handles the signal interrupt (CTRL + C) and sets the stop_flag to True.
    """
    global stop_flag
    stop_flag = True
    print("\nCTRL + C pressed. Stopping...")
    print("Please wait...")


if __name__ == "__main__":
    threads = []
    stop_flag = False
    signal.signal(signal.SIGINT, signal_handler)
    spamRequests(10000, False, 0.05, 3)
