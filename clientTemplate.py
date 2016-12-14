from serviceManagement import SvcManagement

SvcManagement.init()
serviceInfo = SvcManagement.find('namespaceTest/serviceHello')
handler = SvcManagement.bind(serviceInfo)
r = handler.get('/hello/MengYang')
print(r.text)
