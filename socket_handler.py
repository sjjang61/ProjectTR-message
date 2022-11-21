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
            user = user_manager.set_user_info( params['user_id'], params['id'], self )
            user.send_ack_message( { "command" : Command.USER_INFO_ACK.name, "user" : user.user_data } )

        elif cmd == Command.JOIN_ROOM.name:
            room, user = user_manager.join_room( self )

            # 방에 존재하는 전체 사용자 정보 (나에게 : 전체 사용자 정보)
            room_user_list = []
            for room_user in room.user_list:
                room_user_list.append( room_user.user_data )
            user.send_ack_message( { "command" : Command.JOIN_ROOM_ACK.name, "room_id" : room.room_id, "user_list" : room_user_list } )

            # 나를 제외한 방에 있는 기존 사람들에게 메시지 알람 (새로 들어온 정보전송)
            room.broadcast( { "command":Command.SVR_ROOM_USER_JOIN.name, "room_id" : room.room_id, "user" : user.user_data }, user )

            # 인원 풀 상태
            if room.is_full():
                room.broadcast( { "command" : Command.SVR_ROOM_READY.name } )

        elif cmd == Command.START_GAME.name:
            user_manager.send_ack_message(self, Command.START_GAME_ACK.name )

        elif cmd == Command.END_GAME.name:
            # 게임룸 사용자 전체에게 보내야 할지도...
            user_manager.send_ack_message(self, Command.START_END_ACK.name)

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
