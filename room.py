import datetime
import threading
from protocol import Command, get_msg_format

class Room:

    def __init__(self, room_id, max_user_cnt = 2, max_waiting_sec = 30 ):
        self.room_id = room_id
        self.user_list = []
        self.max_user_cnt = max_user_cnt
        self.max_waiting_sec = max_waiting_sec
        self.reset()

    def reset(self):
        print("\t[ROOM] reset, room_id = %r" % (self.room_id))
        self.create_time = datetime.datetime.now()
        self.start_timer()

    def is_joinable(self):
        return self.get_user_cnt() < self.max_user_cnt;

    def is_full(self):
        return self.get_user_cnt() == self.max_user_cnt;


    def get_user_cnt(self):
        return len( self.user_list )

    def is_in_user(self, target_user):
        for user in self.user_list:
            if user == target_user:
                return True
        return False

    def join(self, user ):
        self.user_list.append(user)
        # print("\t[ROOM >> JOIN ] room_id = %r, user_id = %r, user_cnt = %d " % ( self.room_id, user.id, self.get_user_cnt()))
        self.print( 'ROOM >> JOIN ')

    def leave(self, user ):
        # print("\t[ROOM >> LEAVE] room_id = %r, user_id = %r, user_cnt = %d " % ( self.room_id, user.id, self.get_user_cnt() ))
        self.user_list.remove( user )
        self.print('ROOM >> LEAVE ')

    def broadcast(self, data, except_user = None ):
        for user in self.user_list:
            if user != except_user:
                print("\t[ROOM] broadcast, data = %s " % ( data ) )
                user.send_ack_message( data )

    def start_timer(self):
        print("\t[ROOM] Timer start")
        timer = threading.Timer( self.max_waiting_sec, self.expire_waiting_time )
        timer.start()

    def expire_waiting_time(self):
        print("\t[ROOM] Timer end (Expire time)")

        if not self.is_full() :
            for user in self.user_list:
                user.send_ack_message( Command.SVR_GAME_WAITING_EXPIRE.name )
                self.leave( user )

    def print(self, title = 'ROOM_INFO'):
        user_id_list = []
        for user in self.user_list:
            user_id_list.append( user.id )

        print("\t[%s] room_id = %r, User = [ %r ]" % ( title, self.room_id, ",".join( user_id_list )))

    def send_massage(self, cmd, data = {} ):
        for user in self.user_list:
            msg = get_msg_format(cmd, data )
            user.send_message( msg )