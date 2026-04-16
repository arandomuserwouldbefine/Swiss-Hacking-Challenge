## Challenge Description
![[Screenshot 2026-04-16 at 3.49.08 PM.png]]

We are given a python file named `otp_public.py` and a netcat connection
```python
#!/usr/bin/env python3

import secrets

  

FLAG = "FAKE_FLAG"

  

def encrypt(key, plaintext):

return ''.join(str(int(a) ^ int(b)) for a, b in zip(key, plaintext))

  
  

def main():

# keygen

key = format(secrets.randbits(365), 'b')

print("Welcome to the CryptoFarm!")

while True:

command = input('Would you like to encrypt a message yourself [1], get the flag [2], or exit [3] \n>').strip()

try:

if command == "1":

data = input('Enter the binary string you want to encrypt \n>')

print("Ciphertext = ", encrypt(key, data))

key = format(secrets.randbits(365), 'b')

elif command == "2":

print("Flag = ", encrypt(key, format(int.from_bytes(FLAG.encode(), 'big'), 'b')))

elif command == "3":

print("Exiting...")

break

else:

print("Please enter a valid input")

except Exception:

print("Something went wrong.")

  

if __name__ == "__main__":

main()
```

We connect to the service using netcat:
`ncat --ssl <connection>.m0unt41n.ch 31337`
First, we try encrypting a simple input:![[Screenshot 2026-04-16 at 4.52.04 PM.png]]

The service gives us two useful options:
- Encrypt our own message
- Get the encrypted flag
At first this might look random, but this step is actually the key to solving the challenge.

The encryption function is:
`cipher = key ⊕ plaintext
`plaintext = 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`

Then:
`cipher = key ⊕ 0 = key`

After choosing option `[1]`, the key **changes**.  
So the order of actions matters.
We will send bunch of zeroes, here's how:
![[Screenshot 2026-04-16 at 4.58.42 PM.png]]
## Recovering flag

Since we already recovered the key from the previous step, we can simply XOR again:
If we send:
`flag = cipher_flag ⊕ key`
Using the script:

```python
from Crypto.Util.number import long_to_bytes

def xor(a, b):

return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

a = "000001111110100111111101011001111100010101110001001101110101011011100001111010111100001111011101001111001100111011100110010000001111100010100110111110010010010110110001111101010100100000011111001100100110110110101011011001001111100111001001110000010001011110010110100001100010101010101101000011001001011"

b = "111000010011100100111011000000111010010100010101010111111010000001111111001100110000101101100011100100000000010000111010100111100010010001100100010001111011010101110011001111011111011010011101100011001111101100100001110101100100011101000011000010111100010101011100010011001111100001110011110111000110110001001010011010001001011000000001010100101101110000011110011"

b = b[:len(a)]
c = xor(a, b)
c = c.zfill((len(c) + 7) // 8 * 8)

flag = long_to_bytes(int(c, 2))

print(flag)
```
