
## Description
![[Screenshot 2026-04-16 at 5.12.17 PM.png]]

## Source Code Analysis

We are only given 2 files in the tar.gz file: 
1) entrypoint.sh
2) Dockerfile
### Dockerfile

```dockerfile
FROM php:7.4-apache

  

RUN apt-get update && \

apt-get install -y default-mysql-server wget && \

wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -O /usr/local/bin/wp && \

chmod +x /usr/local/bin/wp

  

RUN sed -i 's/^bind-address/#bind-address/' /etc/mysql/my.cnf

  

RUN docker-php-ext-install mysqli pdo pdo_mysql

  

RUN wget https://wordpress.org/wordpress-5.4.1.tar.gz && \

tar -xzf wordpress-5.4.1.tar.gz && \

mv wordpress/* /var/www/html/ && \

rm -rf wordpress wordpress-5.4.1.tar.gz && \

chown -R www-data:www-data /var/www/html

  

COPY entrypoint.sh /usr/local/bin/

COPY ./flag.txt ./flag.txt

RUN chmod +x /usr/local/bin/entrypoint.sh

  

EXPOSE 80

  

ENTRYPOINT ["entrypoint.sh"]

CMD ["apache2-foreground"]

```


1) It installs php:7-4-apache
2) It then updates it's packages and installs mysql-server and wordpress cli
3) It downloads the wordpress from the wordpress official site
4) and sets the flag

### entrypoint.sh

```bash
#!/bin/bash

set -e

  

mysqld_safe &

  

sleep 10

  

if [ ! -d "/var/lib/mysql/wordpress" ]; then

mysql -u root -e "CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;"

mysql -u root -e "CREATE USER 'wordpress'@'localhost' IDENTIFIED BY 'REDACTED';"

mysql -u root -e "GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'localhost';"

mysql -u root -e "FLUSH PRIVILEGES;"

fi

  

apache2-foreground &

  

echo 'Testing MySQL connection...'

mysql -u wordpress -ppassword -h localhost -e "SHOW DATABASES;" && echo "MySQL connection successful." || echo "MySQL connection failed."

  
  

if ! wp --allow-root --path=/var/www/html core is-installed; then

wp --allow-root --path=/var/www/html config create --dbname=wordpress --dbuser=wordpress --dbpass=REDACTED --dbhost="127.0.0.1:3306"

wp --allow-root --path=/var/www/html core install --url="http://127.0.0.1:8000" --title="My WordPress Site" --admin_user="admin" --admin_password="REDACTED" --admin_email="admin@example.com"

wp --allow-root --path=/var/www/html option update home 'http://127.0.0.1:8000'

wp --allow-root --path=/var/www/html option update siteurl 'http://127.0.0.1:8000'

PLUGIN_SLUG="backup-backup"

PLUGIN_VERSION="1.3.7"

wp --allow-root --path=/var/www/html plugin install $PLUGIN_SLUG --version=$PLUGIN_VERSION --activate

fi

  

wait
```

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
