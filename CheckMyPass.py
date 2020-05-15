import requests
import hashlib
import sys

def request_api_data(char):
    url = 'https://api.pwnedpasswords.com/range/' + char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching : {res.status_code}')
    return res

def get_leaked_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1pass[:5], sha1pass[5:]
    response = request_api_data(first5)
    return  get_leaked_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} has been leaked {count} times, better if you change it.')
        else:
            print(f'{password} is safe and not been leaked')

main(sys.argv[1:])

