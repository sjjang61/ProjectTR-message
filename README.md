# ProjectTR-message
- messaging server based on web-socket 


## Structure 
```python
UserManager
[ user ] [ user ] [ user ] [ ... ] 

RoomManager
[ Room [ user, user ], Room [ user, user], ... ]
```

## Protocol
- defined in protocol.py
```python

    # CLI -> SVR
    # SVR -> CLI (xxx_ACK)
    USER_INFO = auto()      # 사용자 정보 전송
    USER_INFO_ACK = auto()

    JOIN_ROOM = auto()      # 룸 입장
    JOIN_ROOM_ACK = auto()

    LEAVE_ROOM = auto()     # 룸 퇴장
    LEAVE_ROOM_ACK = auto()

    START_GAME = auto()     # 게임시작
    START_GAME_ACK = auto()

    END_GAME = auto()       # 정상종료
    END_GAME_ACK = auto

    END_ANORMAL = auto()    # 비정상 종료(에러) : 서버 -> 클라
    
    # SVR -> CLI
    SVR_GAME_WAITING_EXPIRE = auto() # 대기시간 종료
```

