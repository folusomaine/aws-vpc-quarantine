#!/bin/bash

# Sample webpage to confirm access to public ec2 instance
# Go to http://<your-ec2-public-ip> to access the webpage
yum update -y
yum install httpd -y
service httpd start
systemctl enable httpd
cd /var/www/html
echo "<html><body><h1>Hello World!</h1><br><h2>This is a poorly configured workload.</h2></body></html>" > index.html

# Curl malicious DNS domains that are labeled for bitcoin
# CryptoCurrency:EC2/BitcoinTool.B!DNS
dig donate.v2.xmrig.com
dig systemten.org
dig xmr.pool.minergate.com
dig pool.minergate.com
dig dockerupdate.anondns.net
