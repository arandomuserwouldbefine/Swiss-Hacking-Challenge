# Description

![[Pasted image 20240422222206.png]]

# Challenge Links

- [https://8c9225b2-704a-40da-8385-c0c86829139f.ctf.m0unt41n.ch:1337](https://8c9225b2-704a-40da-8385-c0c86829139f.ctf.m0unt41n.ch:1337)  (frontend)
- [https://8c2e0861-9067-41ab-a284-46520bedb268.ctf.m0unt41n.ch:1337](https://8c2e0861-9067-41ab-a284-46520bedb268.ctf.m0unt41n.ch:1337)  (idp)
- [https://e51868a9-d112-4452-aaca-7b5c5f43d27b.ctf.m0unt41n.ch:1337](https://e51868a9-d112-4452-aaca-7b5c5f43d27b.ctf.m0unt41n.ch:1337)  (token)
- [https://d1d7cb27-0b62-4d77-97c1-a5f0035584b6.ctf.m0unt41n.ch:1337](https://d1d7cb27-0b62-4d77-97c1-a5f0035584b6.ctf.m0unt41n.ch:1337)  (back end)


# Analyzing Source Code

In the entrypoing.sh we are given credentials
![[Pasted image 20240422222413.png]]
These email and hashed password (cracked - `password`) will be helpful in logging in.


# Frontend Login Page

![[Pasted image 20240422222519.png]]
Let's authenticate using the credentials we had in the entrypoint.sh
![[Pasted image 20240422222551.png]]
Hurray! We are authenticated. Let's explore further functionalities of this frontend link.

## Analyzing front-end application code

![[Pasted image 20240422222744.png]]
Wow! We can read files off the server, cuz the page parameter isn't sanitised and hence we can read all files from the server. So let's first get the necessary environment variables.

https://8c9225b2-704a-40da-8385-c0c86829139f.ctf.m0unt41n.ch:1337/page?page=../../../proc/self/environ
![[Pasted image 20240422222908.png]]
These two `CLIENT_ID` and `CLIENT_SECRET` are enough for us to proceed futher.

## Analyzing token-exchange's application code

![[Pasted image 20240422223155.png]]

We can determine that the application uses basic authentication which is just base64 of username and password like `username:password`. We have the client_id and client_secret.
There are some easy bypassable checks, we can provide hardcoded grant_type and subject_token_type but we can't just provide directory subject_token, we need to cook up the jwt.

# Generating JWT

> Requirements
> 	We need `kid` which we can get it from the https://{IDP_ENDPOINT}/keys endpoint and `aud` set as `frontend` and `payload` and to get the flag, we need a entry for `name`:`admin` so we need to set that as well.
> 	![[Pasted image 20240422223638.png]]
> 	Putting the secret key as emtpy is cool, because that way the server can decrypt it easily.

![[Pasted image 20240422223749.png]]
Storing it in env variables.

From this blog post we can get the idea how to send the server a correct payload.
https://www.authlete.com/developers/token_exchange/

![[Pasted image 20240422223917.png]]

![[Pasted image 20240422223928.png]]
Boom, we have the jwt token, let's just paste it in our cookie and get the flag from the backend server.
![[Pasted image 20240422224028.png]]
This part of the code just decodes our payload of `name`:`admin` and encodes it using the backend key, which we can use it on the backend side.
![[Pasted image 20240422224115.png]]
Then, it just decodes the token using the back-end key and just checks if the name is equals to admin.

# Flag
https://6f77992a-d336-4a08-a810-05a96d2e965c.ctf.m0unt41n.ch:1337/flag?token=eyJhbGciOiJIUzI1NiIsImtpZCI6ImJhY2tlbmQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiYWRtaW4iLCJhdWQiOiJiYWNrZW5kIn0.MOxVUjMzQipgO7eBbxxwReDr_M5DBseOa6oFdV350rE

![[Pasted image 20240422224216.png]]


