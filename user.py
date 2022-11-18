import json

class User():
    def __init__(self, socketHandler ):
        self.user_id = ''
        self.id = ''
        self.status = 'WAITING' # 'WAITING', 'GAME'
        self.socketHandler = socketHandler

    def set_status(self, status = 'WAITING'):
        self.status = status

    def set_info(self, user_id, id ):
        self.user_id = user_id
        self.id = id

    def send_message(self, msg ):
        self.socketHandler.send_message( msg )

    def send_ack_message(self, msg ):
        data = { "command" : msg }
        self.socketHandler.send_message( json.dumps(data) )

    def print(self):
        print("[USER] user_id = %r, id = %r" % ( self.user_id, self.id ))

