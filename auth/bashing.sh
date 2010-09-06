
read password
article='/Articles/402512/'

content_length=$((27+${#password}))

openssl s_client -connect lwn.net:443 -quiet  > /tmp/$$ <<EOF
POST /login HTTP/1.1
Host: lwn.net
Content-Type: application/x-www-form-urlencoded
Content-Length: $content_length 

Username=RobWilco&Password=$password
EOF

cookie=`sed -n 's/Set-Cookie: \([^\;]*\)\;.*/\1/p' /tmp/$$` 
echo $cookie
echo $article

# openssl s_client -connect lwn.net:443 -quiet <<EOF 
nc lwn.net 80  -q 2 <<EOF
GET $article  HTTP/1.1
Host: lwn.net
Cookie: $cookie

EOF
