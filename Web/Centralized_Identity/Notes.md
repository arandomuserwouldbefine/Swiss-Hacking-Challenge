# Description

![Description](Pasted_image_20240422222206.png)

# Challenge Links

- [Frontend](https://8c9225b2-704a-40da-8385-c0c86829139f.ctf.m0unt41n.ch:1337)
- [IDP](https://8c2e0861-9067-41ab-a284-46520bedb268.ctf.m0unt41n.ch:1337)
- [Token](https://e51868a9-d112-4452-aaca-7b5c5f43d27b.ctf.m0unt41n.ch:1337)
- [Backend](https://d1d7cb27-0b62-4d77-97c1-a5f0035584b6.ctf.m0unt41n.ch:1337)

# Analyzing Source Code

In `entrypoint.sh` we are given credentials:

![entrypoint.sh](Pasted_image_20240422222413.png)

These email and hashed password (cracked as `password`) will be helpful in logging in.

# Frontend Login Page

![Frontend Login Page](Pasted_image_20240422222519.png)

Let's authenticate using the credentials we had in `entrypoint.sh`.

![Authentication](Pasted_image_20240422222551.png)

Hurray! We are authenticated. Let's explore further functionalities of this frontend link.

## Analyzing Front-End Application Code

![Front-End Application Code](Pasted_image_20240422222744.png)

Wow! We can read files off the server, as the `page` parameter isn't sanitized and hence we can read all files from the server. So let's first get the necessary environment variables:

[Read Environment Variables](https://8c9225b2-704a-40da-8385-c0c86829139f.ctf.m0unt41n.ch:1337/page?page=../../../proc/self/environ)

![Environment Variables](Pasted_image_20240422222908.png)

These two `CLIENT_ID` and `CLIENT_SECRET` are enough for us to proceed further.

## Analyzing Token-Exchange's Application Code

![Token-Exchange's Application Code](Pasted_image_20240422223155.png)

We can determine that the application uses basic authentication, which is just base64 of `username:password`. We have the `client_id` and `client_secret`.

There are some easy bypassable checks. We can provide a hardcoded `grant_type` and `subject_token_type` but we can't just provide any subject_token directly; we need to cook up the JWT.

# Generating JWT

> Requirements:
> We need the `kid`, which we can get from the [IDP keys endpoint](https://8c2e0861-9067-41ab-a284-46520bedb268.ctf.m0unt41n.ch:1337/keys), and `aud` set as `frontend`. We also need to include an entry for `name:admin` in the payload to get the flag.
> 
> ![Kid Requirement](Pasted_image_20240422223638.png)
> 
> Setting the secret key as empty is advantageous, as it allows the server to decrypt the token easily.

![JWT](Pasted_image_20240422223749.png)

Storing the JWT in environment variables.

You can follow this [blog post](https://www.authlete.com/developers/token_exchange/) to understand how to send the server a correct payload.

![JWT Generation](Pasted_image_20240422223917.png)

![JWT](Pasted_image_20240422223928.png)

Boom! We have the JWT token. Let's paste it in our cookie and get the flag from the backend server.

![JWT in Cookie](Pasted_image_20240422224028.png)

This part of the code just decodes our payload of `name:admin` and encodes it using the backend key, which we can use on the backend side.

![Decoded Token](Pasted_image_20240422224115.png)

Then, it decodes the token using the backend key and checks if the name equals `admin`.

# Flag

[Get Flag](https://6f77992a-d336-4a08-a810-05a96d2e965c.ctf.m0unt41n.ch:1337/flag?token=eyJhbGciOiJIUzI1NiIsImtpZCI6ImJhY2tlbmQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiYWRtaW4iLCJhdWQiOiJiYWNrZW5kIn0.MOxVUjMzQipgO7eBbxxwReDr_M5DBseOa6oFdV350rE)

![Flag](Pasted_image_20240422224216.png)
