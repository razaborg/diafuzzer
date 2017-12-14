#!/usr/bin/env python2
import sys
sys.path.append('../')
import Diameter as dia
import yaml
from scenario import dwr_handler
import socket as sk

class Config():
    def load(self, confFile):
        conf = self.getConfig(confFile)
        self.checkConfig(conf)
        # checkConfig verifies the configuration and creates self.config
        

    def getConfig(self, confFile):
        raw = ''
        with open(confFile, 'r') as f:
            raw = f.read()
        return yaml.load(raw)

    def checkConfig(self, config):
        # Check for mandatory elements
        assert('diameter-default' in config)
        assert('ip-default' in config)
        #print(config)

        # If everything went fine, we create the config attribute
        self.config = config

    def get(self, level0, level1):
        assert(self.config is not None)
        assert((level0 and level1) is not None)
        assert(level0 in self.config)
        assert(level1 in self.config[level0])

        return (self.config[level0][level1])
    
    def getAll(self, level0):
        assert(self.config is not None)
        assert(level0 in self.config)

        return(self.config[level0])

class Pipe():
    def __init__(self, config):
        assert(isinstance(config, Config))
        s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        local_ip = config.get('ip-default', 'src-ip')
        local_port = config.get('ip-default', 'src-port')
        s.bind((local_ip, local_port))

        remote_ip = config.get('ip-default', 'dst-ip')
        remote_port = config.get('ip-default', 'dst-port')
        s.connect((remote_ip, remote_port))


if __name__ == "__main__":
    # We load the config from config.yml 
    myconf = Config()
    myconf.load('config.yml')

    # We create the pipe to exchange diameter traffic between our scanner and the Diameter device
    trafficPipe = Pipe(myconf)

    
    #print(myconf.get('diameter-default', 'origin-host'))
    #print(myconf.getAll('ip-default'))
