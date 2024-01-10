import requests
import random
import string

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
    'first_name': str(random.randint(1, 100)),
    'last_name': str(random.randint(1, 100)),
    'phone': f'{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
    'email': f'{random.randint(1, 100)}@{random.randint(1, 100)}.{random.randint(1, 100)}',
    'address': str(random.randint(1, 100)),
    'city': str(random.randint(1, 100)),
    'zip': str(random.randint(10000, 99999)),
    'state': 'AL'  # You can modify this according to your needs
}

# Send POST request
response = requests.post(url, headers=headers, data=random_data)

# Print response
print(response.text)
