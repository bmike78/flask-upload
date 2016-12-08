# flask-upload

Flask app to upload multiple files and support multiple users.
* Multithreaded
* Users get their own directory created
* Groups are allowed
* HTTPS via Apache WSGI

Caveats (to be addressed in a future release):
* No AD Auth
* No security for others browsing your directory

## HTTPS
Install httpd and copy the upload-wsgi.conf file to /etc/httpd/conf.d/

```
# yum install httpd
```

Generate certificate:
```

[root@upload flask-upload]# cd /var/www/flask-upload/crt/

(venv)[root@upload crt]# openssl genrsa -des3 -passout pass:x -out server.pass.key 2048; openssl rsa -passin pass:x -in server.pass.key -out server.key; rm server.pass.key; openssl req -new -key server.key -out server.csr
Generating RSA private key, 2048 bit long modulus
...............................+++
...................................................................................+++
e is 65537 (0x10001)
writing RSA key
rm: remove regular file ‘server.pass.key’? y
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:US
State or Province Name (full name) []:VT
Locality Name (eg, city) [Default City]:Burlington
Organization Name (eg, company) [Default Company Ltd]:IPAs for Everyone
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server's hostname) []:upload.domain.com
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
(venv)[root@upload crt]#


[root@upload crt]# openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```
