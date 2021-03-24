#!/usr/bin/python
import cgi
import os
import requests

from youtube_client import YoutubeClient


def get_username_by_id(id):

    header = {"Authorization": f"Bearer {api_token}"}
    api_url = f"https://slack.com/api/users.profile.get?user={user_id}&pretty=1"
    res = requests.get(api_url, headers=header)
    user_name = res.json()['profile']['display_name']

    return user_name


if __name__ == "__main__":
    print('Status: 200')
    print("Content-type: text/plain; utf-8\r\n\r\n")

    api_token = os.environ.get('api_token')

    fs = cgi.FieldStorage()
    video_url = fs["text"].value
    user_id = fs["user_id"].value
    response_url = "https://hooks.slack.com/services/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"

    playlist_id = "PLnqRT9qVgyIDvGJm32xds8BvKwhGJ0526"
    yc = YoutubeClient(playlist_id)

    code, song = yc.add_new_item_to_playlist(video_url)

    user_name = get_username_by_id(user_id)

    payload = {
        "channel": "#성수_신청곡_받습니다",
        "username": "MusicBot",
        "text": f"{user_name}님께서 {song}를 추가하셨습니다.",
        "icon_emoji": ":musical_note:",
    }
    requests.post(
        response_url,
        json=payload,
    )