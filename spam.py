import requests
import random
import string

from faker import Faker
fake = Faker()


# 'Lucy Cechtelar'

fake.address()

url = 'https://www.hhposall.xyz/php/app/index/verify-info.php?t=1704912499601'

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

print(random_data)

# Send POST request
# response = requests.post(url, headers=headers, data=random_data)

# Print response
# print(response.text)

