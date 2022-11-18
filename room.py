import datetime
import threading
from protocol import Command
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

    def get_user_cnt(self):
        return len( self.user_list )

    def join(self, user ):
        self.user_list.append(user)
        # print("\t[ROOM >> JOIN ] room_id = %r, user_id = %r, user_cnt = %d " % ( self.room_id, user.id, self.get_user_cnt()))
        self.print( 'ROOM >> JOIN ')
        # self.broadcast('join')

    def leave(self, user ):
        # print("\t[ROOM >> LEAVE] room_id = %r, user_id = %r, user_cnt = %d " % ( self.room_id, user.id, self.get_user_cnt() ))
        self.user_list.remove( user )
        self.print('ROOM >> LEAVE ')

    def broadcast(self, msg ):
        for user in self.user_list:
            print("\t[ROOM] broadcast, msg = %s " % ( msg ) )
            user.send_message( msg )

    def start_timer(self):
        print("\t[ROOM] Timer start")
        timer = threading.Timer( self.max_waiting_sec, self.expire_waiting_time )
        timer.start()

    def expire_waiting_time(self):
        print("\t[ROOM] Timer end (Expire time)")
        # self.broadcast( "timer end")

        for user in self.user_list:
            user.send_ack_message( Command.SVR_GAME_WAITING_EXPIRE.name )
            self.leave( user )

    def get_msg_format(self, msg ):
        return {
            "command" : "GAME_WAITING_EXPIRE",
            "params" : {}
        }

    def print(self, title = 'ROOM_INFO'):
        user_id_list = []
        for user in self.user_list:
            user_id_list.append( user.id )

        print("\t[%s] room_id = %r, User = [ %r ]" % ( title, self.room_id, ",".join( user_id_list )))
