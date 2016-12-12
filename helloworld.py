#!/usr/bin/python3
from serviceManagement import ServiceManagement as SM
from serviceManagement import rpc
import serviceManagement


class GreetingService:
    name = 'greeting_service'

    @rpc
    def hello(self, name):
        return 'helo, {}'.format(name)

sm = SM()
sm.register('/helloworld', 'amqp://guest:guest@localhost')
sm.run('helloworld')
