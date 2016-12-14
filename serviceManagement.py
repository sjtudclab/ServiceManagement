from kazoo.client import KazooClient
import requests
import atexit
import json
import datetime

class SvcManagement:
    
    class HttpHandler:
        def __init__(self, serviceInfo):
            self.serviceInfo = serviceInfo
            self.ip = serviceInfo['address']

        def addCallNum(self):
            self.serviceInfo['callNum'] = self.serviceInfo['callNum'] + 1
            # del servicePath in serviceInfo
            SvcManagement.zk.set(self.serviceInfo['servicePath'], json.dumps(self.serviceInfo))
    
        def updateLatestCallTime(self):
            self.serviceInfo['latestCallTime'] = str(datetime.datetime.now())
            SvcManagement.zk.set(self.serviceInfo['servicePath'], json.dumps(self.serviceInfo))


        def post(self, url, data=None, json=None, **kwargs):            
            self.addCallNum()
            self.updateLatestCallTime()
            url = 'http://'+self.ip + url
            return requests.post(url, data, json, **kwargs)

        def get(self, url, params=None, **kwargs):
            self.addCallNum()
            self.updateLatestCallTime()
            url = 'http://'+self.ip + url
            return requests.get(url, params, **kwargs)

    prefix = '/services/' 
    @classmethod
    def init(cls, zkAddress='192.168.0.156:2181'):
        cls.zk = KazooClient(hosts=zkAddress)
        cls.zk.start()
        atexit.register(cls.zk.stop)

    @classmethod
    def register(cls, servicePath, value):
        servicePath = self.prefix + servicePath
        if cls.zk.exists(servicePath):
            return False

        cls.zk.create(servicePath, value.encode('UTF-8'), makepath=True)
        
    @classmethod
    def find(cls, servicePath):
        servicePath = cls.prefix + servicePath
        data, stat = cls.zk.get(servicePath)
        data = json.loads(data.decode('UTF-8'))
        data['servicePath'] = servicePath
        return data
    
    @classmethod
    def update(cls, servicePath, value):
        servicePath = cls.prefix + servicePath
        cls.zk.set(servicePath, value)

    @classmethod
    def remove(cls, servicePath):
        servicePath = cls.prefix + servicePath
        cls.zk.delete(servicePath)
    
    @classmethod
    def bind(cls, serviceInfo):
        if serviceInfo['protocol'] == 'http':
            return SvcManagement.HttpHandler(serviceInfo)
'''
    @classmethod
    def findAll(cls, path):        
        services = cls.zk.get_children(path)
        return services 
'''
