#!/usr/bin/python3

import socket
from lab import configuration, mysqldb
import json

def finduser(uid,conn):
    return __finduser(uid,conn.cursor())

def __finduser(uid,cursor):
    cursor.execute("SELECT id, password, nickname FROM USER WHERE id = '%s'" % uid)
    userlist = cursor.fetchall()
    return userlist

def findId(uid, conn):
    return __findId(uid, conn.cursor())

def __findId(uid, cursor):
    cursor.execute("SELECT id FROM USER WHERE id = '%s'" % uid)
    uList = cursor.fetchall()
    return uList

def findPass(uid, conn):
    return __findPass(uid, conn.cursor())

def __findPass(uid, cursor):
    cursor.execute("SELECT password FROM USER WHERE id = '%s'" % uid)
    password = cursor.fetchone()
    return password

def checkLogin(uid, passwd, conn):
    cursor = conn.cursor()
    password = __findPass(uid, cursor)
    if password[0] == passwd:
        return True
    else:
        return False

def insertuser(uid, passwd, nickname,conn):
    cursor = conn.cursor()
    ulist = __finduser(uid,cursor)
    if len(ulist)>0:
        return False
    cursor.execute("INSERT INTO USER VALUES (\'%s\', \'%s\', \'%s\')" % (uid, passwd, nickname))
    return True

def login(uid, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE id = '%s'" % uid)
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for rslt in rv:
        json_data.append(dict(zip(row_headers, rslt)))
    return json.dumps(json_data)

def main():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(('', 8080))
    listen_sock.listen(1)

    while 1:
        conn, addr = listen_sock.accept()
        data = conn.recv(1024)
        d = str(data).split(' ')
        if len(d[1]) == 1:
            conn.sendall('''HTTP/1.1 200 OK
            
            <html><body>Please Sign in or Sign up
            </body>
            </html>'''.encode('utf-8'))
        else:
            log = d[1].strip().split('/')
            if len(log) == 5:
                if __name__ == "__main__":
                    config = configuration.get_db_configuration('config.props')
                    c = mysqldb.get_connection(config)
                    if insertuser(log[2], log[3], log[4], c ) == True:
                        c.commit()
                        conn.sendall('''HTTP/1.1 200 OK
            
                        <html><body>Thank you for signing up!
                        </body>
                        </html>'''.encode('utf-8'))
                    else:
                        conn.sendall('''HTTP/1.1 200 OK
            
                        <html><body>Duplicated ID!
                        </body>
                        </html>'''.encode('utf-8'))
            else:
                if __name__ == "__main__":
                    config = configuration.get_db_configuration('config.props')
                    c = mysqldb.get_connection(config)
                    uList = findId(log[2], c)
                    if len(uList) == 0:
                        conn.sendall('''HTTP/1.1 200 OK
            
                        <html><body>This ID dose not exist
                        </body>
                        </html>'''.encode('utf-8'))
                    else:
                        if checkLogin(log[2], log[3], c) == False:
                            conn.sendall('''HTTP/1.1 200 OK
            
                            <html><body>The password is incorrect
                            </body>
                            </html>'''.encode('utf-8'))
                        else:
                            jsondata = "<html><body>" + login(log[2], c) + "</html></body>"
                            conn.sendall('''HTTP/1.1 200 OK
            
                            '''.encode() + jsondata.encode('utf-8'))

        conn.close()

main()
