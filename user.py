import json

class User():
    def __init__(self, socketHandler ):
        self.user_id = ''
        self.id = ''
        self.user_data = {}
        self.status = 'WAITING' # 'WAITING', 'GAME'
        self.socketHandler = socketHandler

    def set_status(self, status = 'WAITING'):
        self.status = status

    def set_info(self, user_id, id, user_data = {}):
        self.user_id = user_id
        self.id = id
        self.user_data = user_data

    def send_message(self, text ):
        self.socketHandler.send_message( text )

    def send_ack_message(self, obj ):
        self.socketHandler.send_message( json.dumps(obj) )

    def print(self):
        print("[USER] user_id = %r, id = %r, user_data = %r" % ( self.user_id, self.id, self.user_data ))

