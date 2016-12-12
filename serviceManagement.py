#!/usr/bin/python3
from kazoo.client import KazooClient
from nameko.rpc import rpc
from nameko.standalone.rpc import ClusterRpcProxy
import atexit
import os


class ServiceManagement:
    
    def __init__(self, zkAddress='127.0.0.1:2181'):
        self.zk = KazooClient(hosts=zkAddress)
        self.zk.start()
        atexit.register(self.zk.stop)

    def register(self, servicePath, address):
        if self.zk.exists(servicePath):
            return False

        self.zk.create(servicePath, address.encode('UTF-8'), makepath=True)
        

    def find(self, servicePath):
        data, stat = self.zk.get(servicePath)
        return data.decode('UTF-8')

    def update(self, servicePath, address):
        self.zk.set(servicePath, address)

    def remove(self, servicePath):
        self.zk.delete(servicePath)

    def findAll(self, path):
        services = self.zk.get_children(path)
        return services 

    def run(self, serviceName):
        if not self.zk.exists('/instances/' + serviceName):
            self.zk.ensure_path('/instances/' + serviceName)
            def destroy():
                self.zk.delete('/instances/' + serviceName)
            atexit.register(destroy)
            os.system('nameko run ' + serviceName)
 
