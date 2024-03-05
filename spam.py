import random
import requests
import string
import threading
import time
import datetime
import signal
import json

import socks
import socket
from objlog import LogNode, LogMessage
from objlog.LogMessages import Debug, Info, Warn, Error, Fatal

from faker import Faker

fake = Faker()

class MockSlackMessage:
    def __init__(self):
        self.text = "Mocked Slack message"

MUZZLE = True  # Set to True to enable fuzzling, this will not actually send requests and will fake the requests to no real endpoint (for development purposes)

logger = LogNode("Spammer", log_file="spam.log", print_to_console=True, print_filter=[Info, Warn, Error, Fatal])

# pull proxies from file

SOCK5_FILE = 'socks5_proxies.txt'  # Path to the file containing SOCKS5 proxies, one per line (inluding port)
count = 0
startEpochTime = time.time_ns()
# ex:

# 255.255.255.255:9999
# 255.255.255.255:9999
# 255.255.255.255:9999
# etc...

logger.log(Info("Loading SOCKS5 proxies from file..."))
try:
    with open(SOCK5_FILE) as f:
        proxies = f.readlines()
        prox_addresses_full = [x.strip() for x in proxies]
        proxy_addresses = [{'address': prx.split(':')[0], 'port': prx.split(':')[1]} for prx in prox_addresses_full]
except FileNotFoundError:
    logger.log(Error("SOCKS5 proxies file not found. Will continue without proxies."))
    proxy_addresses = []
except Exception as e:
    logger.log(Error("Error loading SOCKS5 proxies from file: " + str(e) + "Will continue without proxies."))
    proxy_addresses = []
else:
    logger.log(Info("Loaded " + str(len(proxy_addresses)) + " proxies"))

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

def sendRequest(runproxy):
    """
    Sends a request to the specified URL with a random number appended to it.
    Uses random data obtained from the getRandom() function.
    Prints the response text received from the server.
    """
    global MUZZLE # for preformance reasons

    global count
    # Set up the SOCKS proxy to route through a public SOCKS5 proxy
    if runproxy and not MUZZLE:
        proxy = randomProxy()
        socks.set_default_proxy(socks.SOCKS5, proxy['address'], int(proxy['port']))
        socket.socket = socks.socksocket

    urlwithnum = url + str(random.randint(1000000000000, 9999999999999))
    random_data = getRandom()
    try:
        if MUZZLE:
            # generate a realistic looking response w/ fake data
            logger.log(Info("Faking request to " + urlwithnum + " with data: " + str(random_data)))
            response = requests.Response()
            response.status_code = 200
            response._content = b'{"status": "success", "message": "Your request has been received and is being processed."}'
        else:
            response = requests.post(urlwithnum, headers=headers, data=random_data)
            logger.log(Info("Sent request to " + urlwithnum + " with data: " + str(random_data) + " and received response: " + response.text))
    except requests.exceptions.ConnectionError:
        logger.log(Warn("Connection error, Skipping request."))
        # remove proxy from list, it's probably dead.
        if runproxy and not MUZZLE:
            proxy_addresses.remove(proxy)
    except requests.exceptions.RequestException as e:
        logger.log(Error("Error sending request: " + str(e)))
    else:
        if response.status_code == 200:
            count += 1
            logger.log(Info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + response.text + " count: " + str(count) + " money wasted: $" + str(count * 0.0025)))
        else:
            logger.log(Error("Received non-200 status code: " + str(response.status_code) + " with response: " + response.text))
minicount = 0
def sendSlackMessage():
    global MUZZLE
    global minicount
    if minicount == 10:
        minicount = 0
        print("Sending slack message...")
        slack_data = {
            "money": str("$" + str(count * 0.0025)),
            "count": str(count)
        }
        print(slack_data)
        if not MUZZLE:
            slack = requests.post('https://hooks.slack.com/triggers/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', data=json.dumps(slack_data))
        else:
            slack = MockSlackMessage()
        logger.log(Debug("Sent slack message with data: " + str(slack_data)))
    else:
        minicount += 1
        logger.log(Debug("Not sending slack message... " + str(minicount) + "/10"))

def getAverageRequestsAndDuration():
  print("Time since start: ")
  currentEpochTime = time.time_ns()
  timeSinceStart = 1
  timeSinceStart = (currentEpochTime - startEpochTime) * 0.000000001 
  print(timeSinceStart)
  print(" seconds, Total requests: ")
  print(count)
  requestsPerSecond = count/timeSinceStart 
  print(", Requests per second(on average): ")
  print(requestsPerSecond)
  print("Done, resuming requests")


def spamRequests(num_requests, infinite, cooldown, cooldown2, proxy):
    """
    Sends a specified number of requests or runs in infinite mode, spamming requests indefinitely.

    Args:
        num_requests (int): The number of requests to send. If less than 100, it will be set to 100.
        infinite (bool): Flag indicating whether to run in infinite mode or not.
        cooldown (float): The cooldown time between each request in seconds.
        cooldown2 (float): The cooldown time between each batch of requests in seconds.
        proxy (bool): Flag indicating whether to use a proxy or not.

    Returns:
        None
    """
    if proxy_addresses == []:
        proxy = False

    if num_requests < 100:
        logger.log(Warn("Number of requests is less than 100, setting to 100."))
        num_requests = 100
    elif infinite == True:
        logger.log(Info("Running in infinite mode."))
        logger.log(Info("cooldown: " + str(cooldown) + " seconds."))
        logger.log(Info("Press CTRL + C to stop."))
        while True:
            if stop_flag:
                break
            for _ in range(100):
                if stop_flag:
                    break
                thread = threading.Thread(target=sendRequest, args=(proxy,))
                thread.start()
                threads.append(thread)
                thread.join()
                time.sleep(cooldown)
            time.sleep(cooldown2)
            sendSlackMessage()
            getAverageRequestsAndDuration()

    else:
        print("Spamming " + str(num_requests) + " requests")
        print("Cooldown between requests: " + str(cooldown) + " seconds")
        for _ in range(int(num_requests / 100)):
            if stop_flag:
                break
            for _ in range(100):
                if stop_flag:
                    break
                thread = threading.Thread(target=sendRequest, args=(proxy,))
                thread.start()
                threads.append(thread)
                time.sleep(cooldown)
            time.sleep(cooldown2)
            sendSlackMessage()
            getAverageRequestsAndDuration()

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
    spamRequests(100000, False, 0.05, 1, False)
