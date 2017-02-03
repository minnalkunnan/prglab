import server
import requests
import MT19937

def ascii_to_hex ( ascii_text ):
   hex_text = ascii_text.encode("hex");
   #print(hex_text)
   return hex_text
   
def hex_to_ascii ( hex_text ):
   ascii_text = hex_text.decode("hex");
   #print(ascii_text)
   return ascii_text
   
def hex_to_base64 ( hex_text ):
   if len(hex_text) % 2 == 1:
      hex_text = "0" + hex_text
   base64_text = hex_text.decode("hex").encode("base64");
   #print(base64_text)
   return base64_text
   
def base64_to_hex ( base64_text ):
   hex_text = base64_text.decode("base64").encode("hex");
   #print(hex_text)
   return hex_text

def get_tokens():
	i = 1
	while (i <= 78):
		token = server.generate_token()
		print("Token " + str(i) + ":" + token + "\n")
		i += 1

def resetPost():
	payload = {'user':'minnal'}
	r = requests.post("http://localhost:8080/forgot", data=payload)
	return r

def parseHTML(s):
	for item in s.split("\n"):
		if "token" in item:
			line = (item.split("token="))[1]
			token = (line.split("<!--close_token-->"))[0]
			return token

def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

def breakToken(y):
	y = y ^ (y >> 18);
	y = y ^ (y << 15) & 0xEFC60000;
	y = y ^ (y << 7) & 0x1680;
	y = y ^ (y << 7) & 0xC4000;
	y = y ^ (y << 7) & 0xD200000;
	y = y ^ (y << 7) & 0x90000000;
	y = y ^ (y >> 11) & 0xFFC00000;
	y = y ^ (y >> 11) & 0x3FF800;
	y = y ^ (y >> 11) & 0x7FF;

	return _int32(y);

def getAsciiValues(t):
	hexToken = base64_to_hex(t)
	asciiToken = hex_to_ascii(hexToken)
	mersenneArray = []
	for item in asciiToken.split(":"):
		mersenneArray.append(item)

	return mersenneArray

def createMersenneState():
	
	mersenneArray = [0] * 624
	i = 0

	while i < 78:
		j = 0
		r = resetPost()
		base64token = parseHTML(r.text)
		temp = getAsciiValues(base64token)
		
		while j < 8:
			mersenneArray[(i * 8) + j] = breakToken(int(temp[j]))
			j += 1

		i += 1

	return mersenneArray

def twist(self):
     for i in range(624):
         # Get the most significant bit and add it to the less significant
         # bits of the next number
         y = _int32((self.mt[i] & 0x80000000) +
                    (self.mt[(i + 1) % 624] & 0x7fffffff))
         self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

         if y % 2 != 0:
             self.mt[i] = self.mt[i] ^ 0x9908b0df
     self.index = 0

def extractToken(mt):
	token = ""
	for i in range(8):
		token += str(mt.extract_number())

		if i != 7:
			token += ":"

	return token

mt = MT19937.MT19937(0)

mersenneState = createMersenneState()
mt.mt = mersenneState

token = extractToken(mt)
token = hex_to_base64(ascii_to_hex(token))
print(token)