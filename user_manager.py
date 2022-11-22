from room_manager import RoomManager
from http_manager import get_user_api, ApiResource
from protocol import Command

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
        user = self.get_user( socketHandler )
        if user != None:
            room = self.room_manager.get_user_room( user )
            if room != None:
                room.leave( user )
                room.broadcast( { "command": Command.SVR_ROOM_USER_DISCONNECT.name, "user" : user.user_data }, user )

            self.user_list.remove(user)
            print("[UserManager] delete user")


    def send_message( self, msg ):
        for user in self.user_list:
            user.send_message( msg )

    def send_message_expept(self, msg, socketHandler ):
        for user in self.user_list:
            if user.socketHandler != socketHandler:
                user.send_message( msg )

    def send_ack_message(self, socketHandler, cmd, data = {} ):
        user = self.get_user(socketHandler)
        user.send_ack_message( cmd, data )

    def get_user_list(self):
        return self.user_list

    def join_room(self, socketHandler ):
        print("[UserManager] Join room")
        user = self.get_user( socketHandler )
        room = self.room_manager.join_room( user )
        return room, user

    def set_user_info(self, user_id, id, socketHandler ):
        user = self.get_user(socketHandler)
        if user != None:
            user_data = get_user_api( ApiResource.USER.name, user_id)
            user.set_info(user_id, id, user_data)
            user.print()

        return user

    def get_user_room(self, socketHandler ):
        user = self.get_user(socketHandler)
        room = self.room_manager.get_user_room( user )
        return room