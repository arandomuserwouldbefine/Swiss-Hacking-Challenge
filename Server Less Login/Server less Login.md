## Challenge Description

![[Pasted image 20240421103439.png]]

## Login Page

![[Pasted image 20240421103502.png]]

## Viewing Source Code

![[Pasted image 20240421103521.png]]
main.py contains the server code and pyscript.json includes the configurations.

![[Pasted image 20240421103554.png]]
Looking at main.py, we can see that we need a valid username and password to get authenticated and get the flag, cuz the query is parameterized and without a master key we won't be able to decrypt the flag.

## pyscript.json

![[Pasted image 20240421103715.png]]
It shows the path to the database.db, can we access it? The answer is yes, we can.

## Opening DB in sqlite3 browser

![[Pasted image 20240421103800.png]]
It is sha256 hash, so let's try to crack the hash using crackstation.net.
![[Pasted image 20240421103830.png]]
It's cracked easily `python`

## Flag

After authenticating with admin and the python as the credentials, we get the flag.
![[Pasted image 20240421103857.png]]

