## Challenge Description
![[Screenshot 2026-04-16 at 2.13.39 PM.png]]

We are given the following attachments: `main.py`and `output.txt`
`output.txt`

```
Public modulus (n): 1186029292037952909983792432306452587425266074685148559256411524118533884795954832993947356308189843827916747393770934033391200656633881903962557992375311329821223845429093776689672634207483637282457856395284891548748666784553146529707500135533133296584880911894111872112018935683414189955943902732488471774953
Public exponent (e): 65537
Encrypted flag: 733568336222790589470096969949196690400886881122508612017162580799729948344126319987475331014669434677564792251353760238087218803592587521385878004071493183548939254573853401155722047457350634791379651022516512709399603944845196902930993851922578027579933013748262257897144604228176365756268938687669643000231
```

`main.py`
```python
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

import random

  

flag = b"SCD{f4k3_fl4g}"

  

p = getPrime(1024)

q = 7

  

n = p * q

  

e = e = 65537

  

phi = (p - 1) * (q - 1)

d = inverse(e, phi)

  

flag_int = bytes_to_long(flag)

ciphertext = pow(flag_int, e, n)

  

print(f"Public modulus (n): {n}")

print(f"Public exponent (e): {e}")

print(f"Encrypted flag: {ciphertext}")

  

decrypt = pow(ciphertext, d, n)

# print(long_to_bytes(decrypt))
```

We’re given an RSA setup with `n`, `e`, and the ciphertext. At first glance, it looks like a normal RSA problem, but looking at the source code reveals a big mistake — one of the primes is hardcoded as `q = 7`.
In RSA, the security depends on `n = p × q` being hard to factor. But here, since `q` is very small and known, factoring `n` becomes trivial:
`p = n // 7`

Once we have both `p` and `q`, we can compute:
`φ(n) = (p - 1)(q - 1)`
Then recover the private key:
`d = e⁻¹ mod φ(n)`

With `d`, we can simply decrypt the ciphertext using:
`m = c^d mod n`

Converting the result back to bytes gives us the flag.



