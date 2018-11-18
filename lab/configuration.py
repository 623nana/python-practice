#!/usr/bin/python3.4
import configparser
def get_configuration(configFile):
    config = configparser.RawConfigParser()
    config.read(configFile)
    return config
def get_db_configuration(configFile, section='DB_DEFAULT'):
    c = get_configuration(configFile)
    return c[section]
if __name__ == "__main__":
    c = get_db_configuration('config.props')
    print(c)
    for key in c:
        print(key)
        print(c[key])