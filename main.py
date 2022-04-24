from datetime import datetime, timedelta
from ssl import SSLContext, DER_cert_to_PEM_cert, PROTOCOL_SSLv23
from socket import create_connection
from json import load
from sys import exit
from OpenSSL.crypto import load_certificate, FILETYPE_PEM  # pyopenssl

filename = "list.json"
try:
    with open(filename) as file:
        website_list = load(file)
except FileNotFoundError:
    print(f"Error: {filename}  not found")
    exit(1)
except Exception as e:
    print(f"Error: {filename} not valid")
    exit(1)
port = 443

for site in website_list:
    conn = create_connection((site, port))
    context = SSLContext(PROTOCOL_SSLv23)
    sock = context.wrap_socket(conn, server_hostname=site)
    cert = DER_cert_to_PEM_cert(sock.getpeercert(True))
    x509 = load_certificate(FILETYPE_PEM, cert)
    end = x509.get_notAfter()
    start = x509.get_notBefore()
    cert_start = datetime.strptime(start.decode('utf-8'), '%Y%m%d%H%M%SZ')
    cert_end = datetime.strptime(end.decode('utf-8'), '%Y%m%d%H%M%SZ')
    now = datetime.now()
    in_three_days = now + timedelta(days=3)

    if in_three_days < cert_end:
        # print("OK : " + site, end="")
        # print(str(cert_start) + " " + str(cert_end))
        pass
    else:
        print("ERROR : " + site, end=" -> ")
        print(str(cert_start) + " " + str(cert_end))
