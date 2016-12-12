#!/usr/bin/python3

from serviceManagement import ServiceManagement as SM
from serviceManagement import rpc
from serviceManagement import ClusterRpcProxy
import serviceManagement
import atexit

sm = SM()
config = {
    'AMQP_URI': sm.find('helloworld')
}

with ClusterRpcProxy(config) as cluster_rpc:
    print(cluster_rpc.greeting_service.hello("hellø") ) # "hellø-x-y"
