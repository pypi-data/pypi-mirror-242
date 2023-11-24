# ros2TCP
Creating a bridge between ROS 2 and TCP Socker

## UNDER DEVELOPMENT


```python
from ros2tcp.plugins import run_server
from ros2tcp.TCPsocket import TCPSocketServer
from ros2tcp.plugins import register_callback, register_service, register_plugin
from std_srvs.srv import SetBool


server = TCPSocketServer()
server.host = 'localhost'
server.port = 2040

request = SetBool.Request()
request.data = True

srv_1 = register_service(
    n_name='test_node_1',
    s_type=SetBool,
    s_name='test_service',
    req=request
)
srv_2 = register_service(
    n_name='test_node_2',
    s_type=SetBool,
    s_name='test_service',
    req=request
)


@register_callback
def my_callback_1(data):
    return data.message + '1'


@register_callback
def my_callback_2(data):
    return data.message + '2'


server.operations = register_plugin(
    srv=srv_1,
    cb=my_callback_1,
    key=1
)

server.operations = register_plugin(
    key=2,
    srv=srv_2,
    cb=my_callback_2
)


run_server(socket=server)

```