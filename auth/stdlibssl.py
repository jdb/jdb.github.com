import socket, ssl, pprint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="client.pem",
                           cert_reqs=ssl.CERT_REQUIRED)

ssl_sock.connect(('localhost', 8000))

print repr(ssl_sock.getpeername())
print ssl_sock.cipher()
print pprint.pformat(ssl_sock.getpeercert())
ssl_sock.close()
