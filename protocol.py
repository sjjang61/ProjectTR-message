import json
from enum import Enum, auto


def get_msg_format(self, cmd, data):
    msg = {
        "command": cmd,
        "data": data
    }
    return json.dumps(msg)

'''
Message Format(json)

1) CLT --> SVR 

{
   "command" : "...",
   "params" : { ... },
}

2) SVR --> CLT  

{
   "command" : "...",
   "params" : { ... },
}
'''

class Command(Enum):
    # CLT -> SVR
    # CONNECT
    USER_INFO = auto()      # 사용자 정보 전송
    USER_INFO_ACK = auto()

    JOIN_ROOM = auto()      # 룸 입장
    JOIN_ROOM_ACK = auto()

    LEAVE_ROOM = auto()     # 룸 퇴장
    LEAVE_ROOM_ACK = auto()

    BROADCAST_ROOM = auto() # 룸 사용자들에게 브로드캐스트 메시지 전송
    BROADCAST_ROOM_ACK = auto()

    START_GAME = auto()     # 게임시작
    START_GAME_ACK = auto()

    END_GAME = auto()       # 정상종료
    END_GAME_ACK = auto

    END_ANORMAL = auto()    # 비정상 종료(에러) : 서버 -> 클라

    # SVR -> CLT
    SVR_ROOM_USER_JOIN = auto()         # 게임룸에 다른 사용자 참가
    SVR_ROOM_READY = auto()             # 게임룸 준비 완료
    SVR_ROOM_USER_DISCONNECT = auto()   # 유저 접속 종료
    SVR_GAME_WAITING_EXPIRE = auto()    # 대기시간 종료

