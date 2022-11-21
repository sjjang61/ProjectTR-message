from settings import API_SERVER
from enum import Enum, auto
import module.http_utils as http

class ApiResource(Enum):
    USER = auto()
    USER_HERO = auto()
    USER_SQUAD = auto()
    MATCH = auto()

def get_api_server( type, user_id = None, hero_id = None, match_id = None ):
    path = get_api_resource( type, user_id, hero_id, match_id )
    return 'http://%s%s' % ( API_SERVER, path )

def get_api_resource( type, user_id = None, hero_id = None, match_id = None ):

    if type == ApiResource.USER.name:
        return '/api/v1/user/{user_id}/'.format( user_id = user_id )
    elif type == ApiResource.USER_HERO.name:
        return "/api/v1/user/{user_id}/hero/{hero_id}/".format( user_id = user_id, hero_id = hero_id)
    elif type == ApiResource.USER_SQUAD.name:
        return "/api/v1/user/{user_id}/squad/{hero_id}/".format( user_id = user_id, hero_id = hero_id)
    elif type == ApiResource.MATCH.name:
        return "/api/v1/match/{match_id}/".format( match_id = match_id )
    else:
        print( "[Error] Unknown api type, type = %s" % ( type ))

def get_user_api( type, user_id ):
    url = get_api_server( type, user_id )
    return http.get( url )


# if __name__ == "__main__":
    # url = get_api_server( ApiResource.USER.name, user_id=1 )
    # print( url )
    # get_user_api( ApiResource.USER.name, user_id=1 )