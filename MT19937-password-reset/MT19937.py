#MERSENNE-TWISTER
#Psuedocode found at: https://en.wikipedia.org/wiki/Mersenne_Twister

import time
import datetime
import calendar
import random

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

def XOR_text_key ( text , key ):
   main_key = key
   new_text = ""
   while len(main_key) < len(text):
      main_key += key
   main_key = main_key[:len(text)]
   hex_text = ascii_to_hex(text)
   hex_key = ascii_to_hex(main_key)
   hex_new_text = hex(int(hex_text, 16) ^ int(hex_key, 16))
   hex_new_text = hex_new_text[2:len(hex_new_text)-1]
   
   if len(hex_new_text) % 2 == 1:
      hex_new_text = "0" + hex_new_text
   new_text = hex_to_ascii(hex_new_text)
   return new_text
   
def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)


#Mersenne Twister MT 19937
class MT19937:
   def __init__(self, seed):
      # Initialize the index to 0
      self.index = 624
      self.mt = [0] * 624
      self.mt[0] = seed  # Initialize the initial state to the seed
      for i in range(1, 624):
         self.mt[i] = _int32(
          1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

   def extract_number(self):
      if self.index >= 624:
         self.twist()

      y = self.mt[self.index]

      # Right shift by 11 bits
      y = y ^ y >> 11
      # Shift y left by 7 and take the bitwise and of 2636928640
      y = y ^ y << 7 & 2636928640
      # Shift y left by 15 and take the bitwise and of y and 4022730752
      y = y ^ y << 15 & 4022730752
      # Right shift by 18 bits
      y = y ^ y >> 18

      self.index = self.index + 1

      return _int32(y)

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
      #test
        
   def invertTwist(self, y):
       #y = self.mt[self.index]

       # Right shift by 11 bits
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
        
def MT_guesser():
   rand = random.randint(5, 60)
   time.sleep(rand)
   
   epoch = int(time.time())
   mt = MT19937(epoch)
   print("Initial time: " + str(epoch))
   
   rand = random.randint(5, 60)
   time.sleep(rand)
   epoch = int(time.time())
   
   num = 0
   while num.bit_length() != 32:
      num = mt.extract_number()
   
   epoch = int(time.time())
   
   print("Finding " + hex_to_base64(format(num, 'x')) + "...")
   epoch = brute_force(epoch, hex_to_base64(format(num, 'x')))
   
   print(epoch)
      
def brute_force(cur_time, base64_in):
  epoch = cur_time

  while epoch:
    mt = MT19937(epoch)

    num = 0
    while num.bit_length() != 32:
      num = mt.extract_number()

    base64 = hex_to_base64(format(num, 'x'))

    #print("I: {} Base64: {}".format(epoch, base64))

    if base64 == base64_in:
      #print("This is the value {}".format(epoch))
      return epoch
      
    epoch -= 1
  return epoch
  
#MT_guesser()

"""
mt = MT19937(8)
mt.twist()
print("mt arr: " + str(mt.mt))
print("index: " + str(mt.index))
print("val: " + str(mt.mt[mt.index]))
y = mt.extract_number()
print("y: " + str(y))
x = mt.invertTwist(y)
print("invert y: " + str(x))
"""
