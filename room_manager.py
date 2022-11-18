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

    def join_room(self, user ):
        room = self.get_joinable_room()
        if room == None:
            print("empty room >> add room")
            room = self.add_room()

        room.join( user )
        room.print()
        # user.send_ack_message( Command.JOIN_ROOM_ACK.name ) # Command.JOIN_ROOM_ACK.value (int)


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

    def send_message(self, target_room, msg ):
        for room in self.room_list:
            if room == target_room:
                print("[RoomManager] send message, ", msg )
                # room.send_message( msg )
