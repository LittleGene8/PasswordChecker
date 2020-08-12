import requests
import hashlib


# checks if api is properly hashed, and then returns response from the API

def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char # Needs to be hashed
	res = requests.get(url)
	
	# If query_char not properly hashed, RuntimeError occurs
	if res.status_code != 200:
		raise RuntimeError(f"Error fetching: {res.status_code}, check the api and try again.")
	return res

# takes the response and converts it into data where it gives you the matching
# hashed passwords and how many time they have been pwned
def get_password_leaks(hashes, hashed_tail):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h == hashed_tail:
			return count	
	return 0


def pwned_password_check(password):
	
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char, tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5_char)
	count_pwned = get_password_leaks(response, tail)

	if count_pwned:
		return f'{password} was found {count_pwned} times'
	else:
		return f'{password} is good to go'

def take_passwords():
	passwords = []
	while True:
		passwords.append(input('Please enter password to check: '))
		again = input('Do you want to check another password (y/n) :')

		if again == 'n':
			break
	return passwords

responses = list(map(pwned_password_check, take_passwords()))

for response in responses:

	print('\n' + response)
