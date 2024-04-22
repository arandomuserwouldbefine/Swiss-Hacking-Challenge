
## Description

![[Pasted image 20240421104621.png]]

## Source Code Analysis

We are only given 2 files in the tar.gz file: 
1) entrypoint.sh
2) Dockerfile
### Dockerfile

![[Pasted image 20240421104803.png]]
1) It installs php:7-4-apache
2) It then updates it's packages and installs mysql-server and wordpress cli
3) It downloads the wordpress from the wordpress official site
4) and sets the flag

### entrypoint.sh

![[Pasted image 20240421104918.png]]
1) Creates databases, set up the username and password, grant privileges
2) Tests the connection
3) hen create db, username and password for wordpress
4) It installs the plugin name **backup-backup** with version **1.3.7**

## Solution 1

There is an RCE in the backup-backup plugin of wordpress and hence we can execute arbitary commands and read the flag

https://github.com/Chocapikk/CVE-2023-6553/tree/main
python3 exploit.py -u https://533f2373-37ca-4b5f-af50-f3e4394573dd.ctf.m0unt41n.ch:1337

running this command we can get the shell and the flag is located at /var/www/html

## Solution 2

We can just directly enter https://533f2373-37ca-4b5f-af50-f3e4394573dd.ctf.m0unt41n.ch:1337/flag.txt
![[Pasted image 20240421105910.png]]