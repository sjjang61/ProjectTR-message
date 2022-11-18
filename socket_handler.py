import json
from user import User
from user_manager import UserManager
from simple_websocket_server import WebSocket
from protocol import Command
user_manager = UserManager()

class SocketHandler(WebSocket):

    def handle(self):
        print('[Message] From : %s, Payload : %s' % ( self.address[0], self.data ))
        msg = json.loads(self.data)
        self.recvMsgHandler(msg['command'], msg['params'])

        # 내가 아닌 사람에게 전송(결과 응답)
        # user_manager.send_message_expept(self.address[0] + u' - ' + self.data, self)


    def recvMsgHandler(self, cmd, params ):
        """
        메시지 처리 및 응답
        cmd (str) : command
        params (object) : json 데이터
        """

        # print( "[RecvMessage] cmd = %r, params = %r" % ( cmd, params ))
        if cmd == Command.USER_INFO.name:
            user_manager.set_user_info( params['user_id'], params['id'], self )
            user_manager.send_ack_message( Command.USER_INFO_ACK.name, self )

        elif cmd == Command.JOIN_ROOM.name:
            user_manager.join_room( self )
            user_manager.send_ack_message( Command.JOIN_ROOM_ACK.name, self )

        elif cmd == Command.START_GAME.name:
            user_manager.send_ack_message(Command.START_GAME_ACK.name, self)

        elif cmd == Command.END_GAME.name:
            # 게임룸 사용자 전체에게 보내야 할지도...
            user_manager.send_ack_message(Command.START_END_ACK.name, self)

        # elif cmd == Command.END_ANORMAL_GAME.name:

        else:
            print('[ERROR] Unknown Command : %s' %( cmd  ))


    def connected(self):
        """
        접속 핸들러
        self (SocketHandler) : socket handler
        """

        print('[JOIN] %s connected' % ( self.address[0] ))
        # 기존 사람들에게 전송
        user_manager.send_message( self.address[0] + u' - connected')

        # 사용자 추가
        user_manager.add_user( User(self) )
        print( 'total %d persons, %s ' % ( len(user_manager.get_user_list()), user_manager.get_user_list() ) )


    def handle_close(self):
        """
        종료 핸들러
        self (SocketHandler) : socket handler
        """

        print( self.address, 'closed' )
        user_manager.del_user( self )
        user_manager.send_message( self.address[0] + u' - disconnected')
