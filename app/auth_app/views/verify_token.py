from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from datetime import datetime as dt
import datetime
import requests
import os

from auth_app.models import U_Config


def get_facebook_access_token():
    try:
        FACEBOOK_ACCESS_TOKEN = U_Config.objects.get(config_name = "FACEBOOK_ACCESS_TOKEN")
        if FACEBOOK_ACCESS_TOKEN.valid_till - dt.now(datetime.timezone.utc) > datetime.timedelta(seconds=1):
            print("Here")
            return FACEBOOK_ACCESS_TOKEN
        FACEBOOK_LONG_LIVE_TOKEN_API = os.getenv("FACEBOOK_LONG_LIVE_TOKEN_API")
        FACEBOOK_LONG_LIVE_TOKEN_API = FACEBOOK_LONG_LIVE_TOKEN_API.replace("{FACEBOOK_APP_ID}", os.getenv("FACEBOOK_APP_ID"))
        FACEBOOK_LONG_LIVE_TOKEN_API = FACEBOOK_LONG_LIVE_TOKEN_API.replace("{FACEBOOK_APP_SECRET}", os.getenv("FACEBOOK_APP_SECRET"))
        response = requests.get(FACEBOOK_LONG_LIVE_TOKEN_API)
        if response.status_code == 200:
            FACEBOOK_ACCESS_TOKEN.config_value = response["access_token"]
            FACEBOOK_ACCESS_TOKEN.valid_till = dt.now() + datetime.timedelta(days=45)
            FACEBOOK_ACCESS_TOKEN.modified_date = dt.now()
            FACEBOOK_ACCESS_TOKEN.save()
            return U_Config.objects.get("FACEBOOK_ACCESS_TOKEN")
        raise ValueError('Can not retrieve accesss token')
    except Exception as e:
        print("Exception: ", e)
        raise ValueError('Can not retrieve accesss token')


def verify_token(token, backend):
    if backend=="google":
        try:
            print("Here")
            CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
            print("Here",CLIENT_ID)
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
            # userid = idinfo['sub']
            # print("UserInformation: ", idinfo)
            return idinfo
        except ValueError:
            # Invalid token
            print("Invalid Token")
            raise ValueError("User profile can not be created")
        except Exception as e:
            print("Exception: ", e)
            raise ValueError('Google verification server error')
    elif backend=="facebook":
        try:
            FACEBOOK_ACCESS_TOKEN = get_facebook_access_token()
            print(FACEBOOK_ACCESS_TOKEN, "lol")
            CLIENT_ID = os.getenv("FACEBOOK_APP_ID", None)
            GRAPH_API = os.getenv("FACEBOOK_GRAPH_API", None)
            GRAPH_API = GRAPH_API.replace("{INPUT_TOKEN}", token)
            GRAPH_API = GRAPH_API.replace("{ACCESS_TOKEN}", FACEBOOK_ACCESS_TOKEN.config_value)

            response = requests.get(GRAPH_API)
            if response.status_code == 200:
                return response.json()
            raise ValueError("User profile can not be created")
        except ValueError:
            # Invalid token
            print("Invalid Token")
            raise ValueError("User profile can not be created")
        except Exception as e:
            print("Exception: ", e)
            raise ValueError('Google verification server error')
