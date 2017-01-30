import server
import requests

def get_tokens():
	i = 1
	while (i <= 78):
		token = server.generate_token()
		print("Token " + str(i) + ":" + token + "\n")
		i += 1

def mypost():
	payload = {'user':'minnal'}
	r = requests.post("http://localhost:8080/forgot", data=payload)
	print(r.status_code)

mypost()