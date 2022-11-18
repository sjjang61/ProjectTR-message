#import asyncio  # 웹 소켓 모듈을 선언한다.
#import websockets  # 클라이언트 접속이 되면 호출된다.

# pip3 install simple_websocket_server
# example : https://pypi.org/project/simple-websocket-server/

from simple_websocket_server import WebSocketServer, WebSocket
from socket_handler import SocketHandler

print("start server...")
server = WebSocketServer('0.0.0.0', 8888, SocketHandler)
server.serve_forever()