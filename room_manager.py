from room import Room
from protocol import Command

class RoomManager:
    def __init__(self):
        self.room_list = []
        self.room_idx = 0

    def get_joinable_room(self):
        for room in self.room_list:
            if room.is_joinable() == True:
                return room

        return None

    def get_user_room(self, user ):
        for room in self.room_list:
            if room.is_in_user( user ) == True:
                return room
        return None


    def join_room(self, user ):
        room = self.get_joinable_room()
        if room == None:
            print("empty room >> add room")
            room = self.add_room()

        room.join( user )
        room.print()
        return room


    def add_room( self ):
        self.room_idx += 1
        room = Room( self.room_idx )
        self.room_list.append( room )
        return room

    def del_room(self, target_room ):
        for room in self.room_list:
            if room == target_room:
                self.room_list.remove( room )
                print("[RoomManager] delete room")
                continue

    # def send_message(self, target_room, msg ):
    #     for room in self.room_list:
    #         if room == target_room:
    #             print("[RoomManager] send message, ", msg )
    #             # room.send_message( msg )

    def send_message(self, target_room, cmd, data, is_except_user = None ):
        for room in self.room_list:
            if room == target_room:
                print("[RoomManager] send message, ", cmd, data  )
                room.broadcast( cmd, data, is_except_user )


    def del_user(self, user ):
        room = self.get_user_room( user )
        room.leave( user )
        self.send_message( room, {} )