#!/usr/bin/python3

import urllib.request
import json
from datetime import datetime
from hw import configuration, mysqldb
import threading
import sys

# config.props
p = sys.argv[1]

def insert(ccn, tcn, price, conn):
    cursor = conn.cursor()
    s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO PRICE_TBL VALUES (\'%s\', \'%s\', \'%s\', %2f)" % (s, ccn, tcn, price))
    return True

def task():
    req = urllib.request

    # 비트코인
    btc = req.urlopen("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR,KRW")
    btc_list = json.loads(btc.read().decode('utf8').replace("'", '"'))

    # 이더리움
    eth = req.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR,KRW")
    eth_list = json.loads(eth.read().decode('utf8').replace("'", '"'))

    # db connection
    config = configuration.get_db_configuration(p)
    c = mysqldb.get_connection(config)

    # 한번씩 커밋이 다 필요할까..?
    for i in btc_list:
        insert('BTC', i, btc_list[i], c)
        c.commit()

    for i in eth_list:
        insert('ETH', i, eth_list[i], c)
        c.commit()
    c.close()

    # 10분마다 실행
    threading.Timer(600, task).start()

def main():
    task()

if __name__=='__main__':
    main()


