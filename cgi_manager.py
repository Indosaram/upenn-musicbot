import cgi
import os
import requests


class CGIManager:
    def __init__(self) -> None:
        self._default_response()
        self.api_token = os.environ.get('api_token')
        
        fs = cgi.FieldStorage()
        self.video_url = fs["text"].value
        self.user_id = fs["user_id"].value

    def get_username_by_id(self):
        header = {"Authorization": f"Bearer {self.api_token}"}
        api_url = f"https://slack.com/api/users.profile.get?user={self.user_id}&pretty=1"
        res = requests.get(api_url, headers=header)
        user_name = res.json()['profile']['display_name']

        return user_name

    def _default_response(self):
        print('Status: 200')
        print("Content-type: text/plain; utf-8\r\n\r\n")
