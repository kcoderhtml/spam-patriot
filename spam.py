import random
import requests
import string
import threading
import time

from faker import Faker
fake = Faker()

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

# Generate random data
def getRandom():
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
    urlwithnum =  url + str(random.randint(1000000000000, 9999999999999))
    random_data = getRandom()
    response = requests.post(urlwithnum, headers=headers, data=random_data)
    print(response.text)



def spamRequests(num_requests, cooldown, cooldown2):
    if num_requests < 100:
        num_requests = 100
    elif num_requests == True:
        threads = []
        while True:
            for _ in range(100):
                thread = threading.Thread(target=sendRequest)
                thread.start()
                threads.append(thread)
                thread.join()
                time.sleep(cooldown)
            time.sleep(cooldown2)

spamRequests(1000, 0.01, 0.5)