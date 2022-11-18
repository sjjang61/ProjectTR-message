import json
from room_manager import RoomManager

class UserManager:
    def __init__(self):
        self.user_list = []
        self.room_manager = RoomManager()

    def get_user(self, socketHandler):
        for user in self.user_list:
            if user.socketHandler == socketHandler:
                return user
        return None

    def add_user(self, user ):
        self.user_list.append( user )
        print("[UserManager] add user, %r, total = %r" % ( user, len( self.user_list ) ))


    def del_user(self, socketHandler ):
        # [to-do]
        # room 에서 속한 정보가 있다면 삭제 처리 필요.
        user = self.get_user( socketHandler )
        if user != None:
            self.user_list.remove(user)
            print("[UserManager] delete user")


    def send_message( self, msg ):
        for user in self.user_list:
            user.send_message( msg )

    def send_message_expept(self, msg, socketHandler ):
        for user in self.user_list:
            if user.socketHandler != socketHandler:
                user.send_message( msg )

    def send_ack_message(self, cmd, socketHandler ):
        user = self.get_user(socketHandler)
        user.send_ack_message( cmd )

    def get_user_list(self):
        return self.user_list

    def join_room(self, socketHandler ):
        print("[UserManager] Join room")
        user = self.get_user( socketHandler )
        self.room_manager.join_room( user )

    def set_user_info(self, user_id, id, socketHandler ):
        user = self.get_user(socketHandler)
        if user != None:
            user.set_info( user_id, id )
            user.print()