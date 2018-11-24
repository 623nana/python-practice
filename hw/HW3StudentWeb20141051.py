#!/usr/bin/python3

import socket
from datetime import datetime
from hw import configuration, mysqldb

def show(type, country, conn):
    day = datetime.now().strftime('%Y-%m-%d')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRICE_TBL WHERE CryptoCurrencyName = \'%s\' AND TargetCurrencyName = \'%s\' AND CurrentTime like '%s%%'" % (type, country, day))
    cList = cursor.fetchall()
    return cList

def main():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(('', 8080))
    listen_sock.listen(1)

    while 1:
        conn, addr = listen_sock.accept()
        data = conn.recv(1024)
        d = str(data).split(' ')
        log = d[1].strip().split('/')

        config = configuration.get_db_configuration('config.props')
        c = mysqldb.get_connection(config)
        tList = show(log[1], log[2], c)
        print(tList)

        print_data = '<html><body>Price List: <br />'
        for i in tList:
            print_data += str(i[0]) + ', ' + str(i[3]) + '<br />'

        print_data += '</body></html>'
        conn.sendall('''HTTP/1.1 200 OK
    
        '''.encode() + print_data.encode('utf-8'))
    conn.close()

if __name__=='__main__':
    main()