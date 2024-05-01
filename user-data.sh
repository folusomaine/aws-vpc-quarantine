#!/bin/bash
# Curl DNS domains that are labeled for bitcoin
# CryptoCurrency:EC2/BitcoinTool.B!DNS
# dig donate.v2.xmrig.com
# dig systemten.org
# dig xmr.pool.minergate.com
# dig pool.minergate.com
# dig dockerupdate.anondns.net
# dig rspca-northamptonshire.org.uk
# dig xmrpool.eu
# dig cryptofollow.com
# dig xmr-usa.dwarfpool.com
# dig xmr-eu.dwarfpool.com
# dig xmr-eu1.nanopool.org

yum update -y
yum install httpd -y
service httpd start
systemctl enable httpd
cd /var/www/html
echo "<html><body><h1>Hello World!</h1><br><h2>I'm a Cloud Developer</h2></body></html>" > index.html